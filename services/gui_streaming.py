import queue
import threading
import time
import random

def stream_worker(llm, messages, chunk_queue):
    try:
        for chunk in llm.stream(messages):
            chunk_queue.put(chunk)
    except Exception as e:
        chunk_queue.put(e)
    finally:
        chunk_queue.put(None)

def stream_response_gui(llm, messages, placeholder):

    # Streams LLM response directly into Streamlit chat UI with a creative,
    # animated loading status (phrases + moving dots) before the first token arrives.

    # Create a thread-safe queue to pass chunks from background to main UI thread
    chunk_queue = queue.Queue()

    # Background worker function to fetch the stream
    # def stream_worker():
    #     try:
    #         for chunk in llm.stream(messages):
    #             chunk_queue.put(chunk)
    #     except Exception as e:
    #         chunk_queue.put(e)
    #     finally:
    #         chunk_queue.put(None)  # Sentinel value indicating the stream is finished

    # Start the stream worker in a background daemon thread
    threading.Thread(target=stream_worker, args=(llm, messages, chunk_queue) ,daemon=True).start()


    # thinking_phrases = random.choice(thinking_phrases_options)
    thinking_phrases = select_thinking_phrase()

    phrase_index = 0
    dot_count = 1
    full_response = ""
    response_started = False

    last_dot_update = time.time()
    last_phrase_update = time.time()

    # Main UI loop
    while True:
        try:
            # Poll the queue with a short timeout to keep the animation fluid
            # This acts as a tiny sleep, preventing high CPU usage
            chunk = chunk_queue.get(timeout=0.05)

            # If sentinel is received, streaming is finished
            if chunk is None:
                break

            # If an exception happened in the background thread, raise it here
            if isinstance(chunk, Exception):
                raise chunk

            # Clear the loading text when the first actual token arrives
            if not response_started:
                full_response = ""
                response_started = True

            # Append content and update UI with the blinking cursor
            if hasattr(chunk, "content") and chunk.content:
                full_response += chunk.content
                placeholder.markdown(full_response + "▌")

        except queue.Empty:
            # The queue is empty (meaning we are still waiting for the first word or next chunk)
            if not response_started:
                now = time.time()

                # 1. Update the dot count every 0.4 seconds (e.g., ".", "..", "...")
                if now - last_dot_update > 0.4:
                    dot_count = (dot_count % 3) + 1
                    last_dot_update = now

                # 2. Cycle to the next fun phrase every 1.8 seconds
                if now - last_phrase_update > 1.8:
                    phrase_index = (phrase_index + 1) % len(thinking_phrases)
                    last_phrase_update = now
                    dot_count = 1  # Reset dots when text changes


                display_thinking_animation(placeholder, thinking_phrases, phrase_index, dot_count)

    # Final render without the cursor element
    placeholder.markdown(full_response)

    return full_response




def select_thinking_phrase():

     # --- Creative Thinking Themes ---
    thinking_phrases_options = [
        [
            "🛒 Gathering fresh ingredients",
            "🔪 Chopping up the context",
            "🌡️ Preheating the language model",
            "🥣 Mixing the concepts together",
            "🍲 Simmering the thoughts",
            "🍳 Cooking up a perfect reply",
            "🍽️ Plating the final response",
        ],
        [
            "📡 Establishing uplink",
            "💾 Downloading subroutines",
            "⚡ Overclocking cores",
            "🧠 Synthesizing synapses",
        ],
        [
            "🔮 Gazing into crystal ball",
            "📜 Reading ancient scrolls",
            "🧪 Brewing cognitive potion",
            "✨ Channeling mana",
        ],
    ]

    return random.choice(thinking_phrases_options)

    

def display_thinking_animation(placeholder, thinking_phrases, phrase_index, dot_count):
    current_phrase = thinking_phrases[phrase_index]
    dots = "." * dot_count
    placeholder.markdown(f"*{current_phrase}{dots}*")
