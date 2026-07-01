import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from backend.core.llm import get_llm
from backend.database.chat_repository import ChatRepository
from backend.tools.tavily_tool import search_tavily
from backend.tools.wikipedia_tool import search_wikipedia
from backend.tools.arxiv_tool import search_arxiv
from backend.tools.duckduckgo_tool import search_duckduckgo
from backend.core.logger import logger


llm = get_llm()


class ChatService:
    """Service for handling chat with intelligent tool-calling."""

    def __init__(self):
        self.msg_repo = ChatRepository()

    def _should_search(self, message: str) -> bool:
        """Decide if web search is needed. Returns True for real-time queries."""
        msg_low = message.lower()
        
        # Real-time keywords that always trigger search
        realtime_keywords = [
            "today", "current", "now", "latest", "recent",
            "price", "weather", "news", "trend", "trending",
            "updates", "rate", "live", "yesterday", "tomorrow",
            "this week", "this month", "this year",
            "breaking", "update", "announce", "released", "launch",
            "stock", "crypto", "bitcoin", "ethereum", "gold",
            "dollar", "euro", "rupee", "yen", "pound",
            "covid", "virus", "disease", "outbreak",
            "election", "vote", "political", "government",
            "sports", "match", "score", "game",
            "movie", "release", "show", "episode",
            "event", "festival", "conference",
        ]
        
        # Check if any keyword matches
        if any(k in msg_low for k in realtime_keywords):
            logger.info("Real-time keyword detected - using tools")
            return True
        
        # Ask LLM for nuanced decision
        check_prompt = f"""Does this question ask for real-time or frequently-changing information?

Examples that need search: "What's the weather?", "Bitcoin price?", "Latest news about X?"
Examples that don't: "How does gravity work?", "What is Python?", "Explain ML"

Question: {message}

Answer with ONLY "yes" or "no"."""
        
        try:
            response = llm.invoke(check_prompt)
            answer = response.content.strip().lower()
            llm_decision = "yes" in answer or "true" in answer
            
            if llm_decision:
                logger.info("LLM: Using tools")
            else:
                logger.debug("LLM: Using LLM only")
            
            return llm_decision
        except Exception as e:
            logger.warning(f"Decision error: {e}, using heuristic")
            return False

    def _search_web(self, query: str) -> str:
        """Search web using Tavily, DuckDuckGo, Wikipedia, and ArXiv."""
        tools = {
            "Tavily": search_tavily,
            "DuckDuckGo": search_duckduckgo,
            "Wikipedia": search_wikipedia,
            "ArXiv": search_arxiv,
        }

        results = []
        per_tool_timeout = 5.0
        total_timeout = 8.0

        logger.debug(f"Searching tools for: {query[:60]}...")
        
        start = time.monotonic()
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(fn, query): name for name, fn in tools.items()}

            try:
                for future in as_completed(futures.keys(), timeout=total_timeout):
                    name = futures[future]
                    try:
                        result = future.result(timeout=per_tool_timeout)
                        if result and not result.startswith("["):
                            results.append(result)
                            logger.debug(f"{name}: OK")
                    except Exception as e:
                        logger.debug(f"{name}: Error - {e}")

                    if len(results) >= 2:
                        break
            except Exception as e:
                logger.warning(f"Search error: {e}")

        if not results:
            logger.warning(f"Tools found no results")
            return ""
        
        logger.info(f"Got results from {len(results)} tools")
        return "\n\n".join(results)

    def chat(self, session_id: str, message: str, use_search: bool = None) -> str:
        """Chat with optional web search for real-time queries."""
        
        # Save message
        self.msg_repo.add_message(session_id, "user", message)

        # Get history
        messages = self.msg_repo.get_messages(session_id)
        formatted_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages[-20:]
        ]

        # Decide: use search?
        if use_search is None:
            should_search = self._should_search(message)
        else:
            should_search = use_search

        # Search if needed
        if should_search:
            logger.info(f"Using tools for: {message[:50]}...")
            web_context = self._search_web(message)
            
            if web_context:
                logger.info(f"Got results - adding to LLM context")
                formatted_messages.append({
                    "role": "system",
                    "content": f"Current web search results:\n{web_context}\n\nUse this to answer the user's question accurately."
                })
            else:
                logger.warning(f"Tools returned no results")
        else:
            logger.debug("Using LLM only")

        # Get LLM response
        response = llm.invoke(formatted_messages)
        answer = response.content

        # Save response
        self.msg_repo.add_message(session_id, "assistant", answer)

        return answer