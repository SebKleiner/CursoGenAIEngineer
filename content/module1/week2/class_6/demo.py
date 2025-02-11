import logging
import os
from typing import List, Dict

from openai import OpenAI

MODEL_TEMPERATURE = 0
REPLY_MAX_TOKENS = 1000

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class OpenaiConnector:
    def __init__(self, api_key: str) -> None:
        os.environ["OPENAI_API_KEY"] = api_key
        self.total_tokens_consumed = 0
        self.client = OpenAI()
        logging.info("OpenaiConnector initialized.")

    def get_gpt_reply(self, prompt: List[Dict[str, str]], model: str = 'gpt-4o-mini',
                      temperature: float = MODEL_TEMPERATURE, max_tokens: int = REPLY_MAX_TOKENS) -> str:
        logging.info(f"Sending request to GPT-4o with prompt: {prompt}")
        response = self.client.chat.completions.create(
            model=model,
            messages=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        logging.info("Received response from GPT-4o.")
        return response.choices[0].message.content


OPEN_AI_KEY = os.getenv('OPENAI_API_KEY')
OPEN_AI_CONNECTOR = OpenaiConnector(api_key=OPEN_AI_KEY)


def sequential_chaining():
    logging.info("Starting sequential chaining.")
    text_to_summarize = """
    Large Language Models (LLMs) have shown remarkable capabilities in generating text,
    translating languages, and answering complex questions. They rely on architectures like Transformers
    and massive training datasets to learn statistical patterns.
    """

    summary_prompt = [
        {"role": "user", "content": f"Summarize the following text in 2-3 sentences:\n{text_to_summarize}"}]
    summary = OPEN_AI_CONNECTOR.get_gpt_reply(summary_prompt)
    logging.info(f"Generated summary: {summary}")

    keywords_prompt = [{"role": "user", "content": f"Extract 5 relevant keywords from this summary:\n{summary}"}]
    keywords = OPEN_AI_CONNECTOR.get_gpt_reply(keywords_prompt)
    logging.info(f"Extracted keywords: {keywords}")

    blog_prompt = [{"role": "user", "content": f"Write a short tech blog paragraph using these keywords: {keywords}"}]
    blog_paragraph = OPEN_AI_CONNECTOR.get_gpt_reply(blog_prompt)
    logging.info(f"Generated blog paragraph: {blog_paragraph}")


def branching_chaining():
    logging.info("Starting branching chaining.")
    user_question = "Who won the last World Cup in soccer?"

    classify_prompt = [
        {"role": "user", "content": f"Classify this question into 'sports' or 'politics':\n{user_question}"}]
    topic_classification = OPEN_AI_CONNECTOR.get_gpt_reply(classify_prompt)
    logging.info(f"Classified topic: {topic_classification}")

    if "sport" in topic_classification.lower():
        response_prompt = [{"role": "user", "content": f"Answer this sports question: {user_question}"}]
    elif "politic" in topic_classification.lower():
        response_prompt = [{"role": "user", "content": f"Answer this politics question: {user_question}"}]
    else:
        response_prompt = [{"role": "user", "content": f"Provide a general answer: {user_question}"}]

    final_answer = OPEN_AI_CONNECTOR.get_gpt_reply(response_prompt)
    logging.info(f"Final answer: {final_answer}")


def iterative_chaining():
    logging.info("Starting iterative chaining.")
    original_text = """
    Large Language Models are extremely powerful for various tasks like text generation,
    translation, summarization, question answering, and more. However, they can also
    produce errors or hallucinations, so human oversight is essential.
    """

    def get_word_count(text):
        return len(text.split())

    current_text = original_text
    word_limit = 1
    max_iterations = 10

    for i in range(max_iterations):
        refine_prompt = [
            {"role": "user", "content": f"Rewrite this text in fewer than {word_limit} words:\n{current_text}"}]
        current_text = OPEN_AI_CONNECTOR.get_gpt_reply(refine_prompt)
        logging.info(f"Iteration {i + 1}: {current_text}")
        if get_word_count(current_text) <= word_limit:
            logging.info("Text meets word limit.")
            break


def hierarchical_chaining():
    logging.info("Starting hierarchical chaining.")
    outline_prompt = [{"role": "user", "content": "Provide a concise outline for an article about 'AI in Healthcare'. Only give 5 main points each main point in a different line. Dont add any other text"}]
    outline = OPEN_AI_CONNECTOR.get_gpt_reply(outline_prompt)
    logging.info(f"Generated outline: {outline}")

    sections = outline.split("\n")
    logging.info(f"Expanding sections: {sections}")

    expanded_sections = []

    for section in sections:
        expand_prompt = [{"role": "user", "content": f"Expand this outline item into a detailed paragraph:\n{section}"}]
        expanded_text = OPEN_AI_CONNECTOR.get_gpt_reply(expand_prompt)
        expanded_sections.append(expanded_text)
        logging.info(f"Expanded section: {expanded_text}")

    merge_prompt = [{"role": "user",
                     "content": "Combine these paragraphs into a cohesive article:\n" + "\n\n".join(expanded_sections)}]
    final_article = OPEN_AI_CONNECTOR.get_gpt_reply(merge_prompt)
    logging.info(f"Final merged article: {final_article}")


def hierarchical_plus_loop_chaining():
    #Consigna: Agreagar validacion a cada una de las secciones del articulo de forma tal que  reduzca la cantidad de palabras a un minimo

    logging.info("Starting hierarchical chaining.")
    outline_prompt = [{"role": "user", "content": "Provide a concise outline for an article about 'AI in Healthcare'. Only give 5 main points each main point in a different line. Dont add any other text"}]
    outline = OPEN_AI_CONNECTOR.get_gpt_reply(outline_prompt)
    logging.info(f"Generated outline: {outline}")

    sections = outline.split("\n")
    logging.info(f"Expanding sections: {sections}")

    expanded_sections = []

    for section in sections:
        expand_prompt = [{"role": "user", "content": f"Expand this outline item into a detailed paragraph:\n{section}"}]
        expanded_text = OPEN_AI_CONNECTOR.get_gpt_reply(expand_prompt)
        expanded_sections.append(expanded_text)
        logging.info(f"Expanded section: {expanded_text}")

    merge_prompt = [{"role": "user",
                     "content": "Combine these paragraphs into a cohesive article:\n" + "\n\n".join(expanded_sections)}]
    final_article = OPEN_AI_CONNECTOR.get_gpt_reply(merge_prompt)
    logging.info(f"Final merged article: {final_article}")



def main():
    # sequential_chaining()
    # branching_chaining()
    # iterative_chaining()
    # hierarchical_chaining()
    hierarchical_plus_loop_chaining()

logging.info("Starting main execution.")
main()
