from backend.core.llm import get_llm
from backend.database.chat_repository import ChatRepository
from backend.tools.tavily_tool import search_tavily
from backend.tools.wikipedia_tool import search_wikipedia
from backend.tools.arxiv_tool import search_arxiv
from backend.tools.duckduckgo_tool import search_duckduckgo


llm = get_llm()


class ChatService:

    def __init__(self):
        self.msg_repo = ChatRepository()

    def _should_search(self, message: str) -> bool:
        """Use LLM to intelligently decide if web search is needed for ANY question"""
        # Heuristic check for obvious real-time keywords
        msg_low = message.lower()
        realtime_keywords = [
            "today",
            "current",
            "now",
            "latest",
            "recent",
            "price",
            "weather",
            "news",
            "trend",
            "trending",
            "updates",
            "rate",
            "live",
        ]
        heuristic = any(k in msg_low for k in realtime_keywords)

        # Ask the LLM a specific question about whether this needs current data
        check_prompt = f"""You are a research assistant.

Does this question ask for information that is LIKELY TO CHANGE or requires CURRENT/REAL-TIME DATA?

Examples that need search:
- "What's the weather today?"
- "What's the Bitcoin price right now?"
- "Tell me the latest AI news"
- "What happened in the news today?"
- "Current unemployment rate?"
- "Is there a cure for X yet?"
- "What's trending on social media?"
- "What are the latest developments in technology?"
- "Tell me about current events"

Examples that DON'T need search:
- "What is photosynthesis?"
- "How does gravity work?"
- "Explain machine learning"
- "What is Python?"
- "How do plants grow?"

Question: {message}

Answer with ONLY "yes" or "no". Think carefully about whether this asks for current/changing information."""
        
        try:
            response = llm.invoke(check_prompt)
            answer = response.content.strip().lower()

            # Check if response indicates yes
            llm_decision = "yes" in answer or "true" in answer

            should_search = heuristic or llm_decision

            reason = "HEURISTIC" if heuristic and not llm_decision else ("LLM" if llm_decision and not heuristic else "HEURISTIC+LLM" if heuristic and llm_decision else "NONE")
            print(f"[LLM DECISION] {reason} → {'Using tools' if should_search else 'LLM only'} for: {message}")

            return should_search
        except Exception as e:
            print(f"[LLM DECISION ERROR] {str(e)} → Using HEURISTIC={heuristic} for: {message}")
            # On error, fall back to the heuristic decision
            return heuristic

    def _search_web(self, query: str):
        """Search web for relevant information"""
        # Run multiple tool searches in parallel with timeouts to reduce latency
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import time

        tools = {
            "Tavily": search_tavily,
            "Wikipedia": search_wikipedia,
            "ArXiv": search_arxiv,
            "DuckDuckGo": search_duckduckgo,
        }

        results = []
        futures = {}

        per_tool_timeout = 3.0  # seconds per tool
        total_timeout = 5.0  # max total seconds to wait for all tools

        start = time.monotonic()
        with ThreadPoolExecutor(max_workers=len(tools)) as executor:
            for name, fn in tools.items():
                futures[executor.submit(fn, query)] = name

            try:
                for future in as_completed(futures.keys(), timeout=total_timeout):
                    name = futures[future]
                    try:
                        tool_start = time.monotonic()
                        result = future.result(timeout=per_tool_timeout)
                        dur = time.monotonic() - tool_start
                        print(f"[PERF] {name} search took {dur:.2f}s")
                        if result:
                            results.append(result)
                    except Exception as e:
                        print(f"[TOOL ERROR] {name}: {e}")
                        results.append(f"[{name} Error: {e}]")

                    # stop if we've exceeded total timeout
                    if time.monotonic() - start > total_timeout:
                        print("[SEARCH] total timeout reached, stopping collection")
                        break
            except Exception as e:
                # as_completed can raise if overall timeout hits
                print(f"[SEARCH] tools timed out or failed: {e}")

        return "\n".join(results) if results else ""

    def chat(self, session_id: str, message: str, use_search: bool = None):

        # 1. Save user message
        self.msg_repo.add_message(
            session_id,
            "user",
            message
        )

        # 2. Get chat history
        messages = self.msg_repo.get_messages(session_id)

        formatted_messages = []

        for msg in messages[-20:]:
            formatted_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # 3. Decide if search is needed
        # If use_search is explicitly set, use that value
        # Otherwise, let the LLM decide
        if use_search is None:
            should_search = self._should_search(message)
        else:
            should_search = use_search

        # 4. Optional: Search web if needed
        if should_search:
            web_context = self._search_web(message)
            
            if web_context:
                formatted_messages.append({
                    "role": "system",
                    "content": f"Current web search results:\n{web_context}\n\nUse this information to provide accurate, current answers."
                })

        # 5. Call LLM to generate response
        response = llm.invoke(formatted_messages)

        answer = response.content

        # 6. Save assistant response
        self.msg_repo.add_message(
            session_id,
            "assistant",
            answer
        )

        return answer