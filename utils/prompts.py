from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate

################
## SUMMARIZER ##
################

class Contribution(BaseModel):
    headline: str = Field(..., description="Headline of the main contribution.")
    description: str = Field(..., description="Description of the main contribution.")


class Takeaways(BaseModel):
    headline: str = Field(..., description="Headline of the main takeaway.")
    description: str = Field(..., description="Description of the main takeaway.")
    applied_example: str = Field(
        ..., description="Applied example related to the main takeaway."
    )


class PaperReview(BaseModel):
    main_contribution: Contribution = Field(
        ..., description="The main contribution of the paper."
    )
    takeaways: Takeaways = Field(..., description="The main takeaways from the paper.")
    category: str = Field(..., description="The primary focus category of the paper.")
    novelty_analysis: str = Field(..., description="Analysis of the paper's novelty.")
    novelty_score: int = Field(
        ..., description="Score representing the novelty of the paper."
    )
    technical_analysis: str = Field(
        ..., description="Analysis of the paper's technical depth."
    )
    technical_score: int = Field(
        ..., description="Score representing the technical depth of the paper."
    )
    enjoyable_analysis: str = Field(
        ..., description="Analysis of the paper's readability and engagement level."
    )
    enjoyable_score: int = Field(
        ..., description="Score representing the enjoyability of reading the paper."
    )


SUMMARIZER_SYSTEM_PROMPT = """
As an applied AI researcher specialized in the field of Large Language Models (LLMs), you are currently conducting a survey of the literature, building a catalogue of the main contributions and innovations of each paper, determining how they can be applied to build systems or create new products. This catalogue will be published by a prestigious organization and will serve as the foundation for all applied LLM knowledge going forward. Now, carefully read the following paper:

WHITEPAPER

{paper_content}

========================

Now answer the following questions:

1. What is the `main_contribution` of this paper? (1 line headline + 8-12 sentences)
    - Be precise. If a new algorithm or technique is introduced, describe its workings clearly and step by step.
    - Do not assume that the reader knows the meaning of new terminology presented in the paper or complex concepts. 
    - Ensure that your answer provides practical insights that offer a solid understanding of the paper.
    - Detail the benefits or advantages of these contributions, along with the real world implications for an LLM practitioner.

2. What is the main `takeaway`? (1 line headline + 8-12 sentences)
    - Focusing on the paper's contributions, explain how they can be used to create an interesting LLM application, improve current workflows, or increase efficiency when working with LLMs.
    - If different models were evaluated and their performance recorded, please note this and its practical implications (in detailed manner, i.e.: which model is best for what).
    - Be very precise, practical and specific as possible. Eliminate any irrelevant content from the paper's applied perspective.
    - Always provide a minimal but detailed applied example related to the takeaway.

3. Which category best describes this paper's primary focus? Choose one from the following options, with "OTHER" being the least desirable choice.
    a. "TRAINING": Discussions on LLM training methods, technical stack improvements, alternative training routines, etc.
    b. "FINE-TUNING": Discussions on fine-tuning, re-training, and specialization of LLMs.
    c. "ARCHITECTURES": Discussions on new LLM architectures, neural network components, etc., excluding prompting or computational systems to manage LLMs.
    d. "PROMPTING": Discussions on prompting methods, agent architectures, etc.
    e. "USE CASES": Discussions on LLM use in specific tasks, such as summarization, question answering, stock prediction, etc.
    f. "BEHAVIOR": Discussions on LLM behavior, including probing, interpretability, risks, biases, emerging abilities, etc.
    g. "OTHER": None of the above.

4. On a scale from 1 to 3, how novel is this paper? (1: not novel, 2: incrementally novel, 3: very novel)
    - Compare the paper's findings and contributions with what is presented in previous and related work. How unique and significant are the findings?
    - Pay close attention to the comparison with prior work and the degree of difference in the author's contributions.
    - Very few papers achieve the '3: very novel' category.

5. On a scale from 1 to 3, how technical is this paper? (1: not technical, 2: somewhat technical, 3: very technical)
    a) A very technical paper is difficult for a non-expert to understand, requires considerable technical knowledge, is filled with equations and jargon, and demands advanced mathematical knowledge.
    b) A somewhat technical paper may be challenging for a layman but can be understood reasonably well by someone with a computer science background. These papers, while not overly complex, explain processes in great detail and are practical and applicable (can be replicated).
    c) A non-technical paper is understandable for anyone with a college degree. These papers often discuss generalities, and the takeaways are more conceptual than technical.

6. On a scale from 1 to 3, how enjoyable is this paper? (1: hard to read, 2: ok, 3: a delight)
    a) A delightful paper is creative, well-written, organized, and presents a novel and intriguing contribution. Few papers achieve this mark.
    b) An 'ok' paper is primarily plain and unexciting but is easy to read and contains some interesting parts. Most papers fall on this category.
    c) A non-enjoyable paper is difficult to read, poorly written, and lacks meaningful, practical, and insightful content.

When assigning numerical ratings consider these guidelines:
- Rating 3/3: (EXCEPTIONAL) Only 10% of papers fall into this category., the paper must be truly exceptional for this.
- Rating 2/3: (COMMON) Most papers (50%) fall into this category.
- Rating 1/3: (RARE) Around 40% of papers belong to this category.

Pay attention to the following:
- Do not repeat the same comments across different answers. 
- Make your "applied_example" different from the ones presented in the paper, and headlines different from the title. 
- Make sure your answers are coherent, clear and truthful.
- Be objective in your assessment and do not praise the paper excessively.

Use the JSON format as in the following examples to respond.

EXAMPLE 1
==========
```
{{
    "main_contribution": {{
        "headline": "Chain-of-Thought (CoT) boosts LLM accuracy in financial sentiment analysis",
    "description": "The paper introduces the Chain-of-Thought (CoT) prompting technique for Large Language Models (LLMs) specifically targeting financial sentiment analysis. The core of CoT lies in its deviation from direct predictions. Instead, it guides the model to build a sequence of interconnected thoughts leading to an accurate sentiment score. In a comparative study, LLMs equipped with CoT achieved a 94% accuracy, surpassing the established FinBERT's 88% and the naive prompting model's 81%."
    }},
    "takeaways": {{
        "headline": "CoT opens new, efficient avenues for LLMs in financial analysis",
        "description": "Using the CoT prompting technique, LLMs can achieve enhanced accuracy in financial news sentiment analysis, ultimately refining stock market predictions. This method not only improves prediction accuracy but also renders the model's thought process transparent. When pitted against FinBERT, the LLM with CoT demonstrated superior performance, signaling its potential dominance in financial analysis tasks.",
        "applied_example": "When processing a news snippet like 'Company X has strong Q3 earnings', an LLM with CoT could generate: 'Strong Q3 earnings -> Likely effective management -> Expected investor trust growth -> Potential bullish market -> Possible stock price ascent.' This layered output simplifies decision-making for market analysts."
    }},
    "category": "USE CASES",
    "novelty_analysis": "The paper extends the boundaries of current research by applying LLMs to financial news sentiment analysis. The introduction of the CoT prompting technique, tailored specifically for this application, represents an incremental advancement in the field.",
    "novelty_score": 2,
    "technical_analysis": "While the paper discusses a computational framework for managing LLM inputs and outputs, it does not delve into complex mathematical theories or algorithms, making it accessible to a wider audience.",
    "technical_score": 1,
    "enjoyable_analysis": "The engaging narrative style, coupled with practical insights, makes the paper an enjoyable read. It balances technical details with easily digestible information and an interesting practical application.",
    "enjoyable_score": 2
}}
```

EXAMPLE 2
==========
```
{{
    "main_contribution": {{
        "headline": "Zero-shot Prompting Technique for GPT-4 Code Interpreter",
        "description": "This paper proposes a zero-shot prompting technique for GPT-4 Code Interpreter that explicitly encourages the use of code for self-verification, which further boosts performance on math reasoning problems. They report a positive correlation between the better performance of GPT4-Code and the higher Code Usage Frequency. Initial experiments show that GPT4-Code achieved a zero-shot accuracy of 69.7% on the MATH dataset which is an improvement of 27.5% over GPT-4’s performance (42.2%)."
    }},
    "takeaways": {{
        "headline": "Leveraging Self-verification and Code Execution in LLMs",
        "description": "Self-verification is already a powerful approach to enhance the performance of LLMs on many tasks but this approach leverages the evaluation of code execution which could make it interesting to solve other kinds of problems. This work highlights the importance of code understanding and generation capabilities in LLMs.",
        "applied_example": "Some of the ideas presented in this paper (specifically, the code-based self-verification and verification-guided weighted majority voting technique) can lead to building high-quality datasets that could potentially help improve the mathematical capabilities in open-source LLMs like Llama 2."
    }},
    "category": "PROMPTING",
    "novelty_analysis": "The research innovative ly combines LLMs with code-based self-verification, achieving a 20% boost over state-of-the-art coding task accuracies. This method's practicality is evident, with tests showing a 30% reduction in coding errors, redefining efficiency in LLM-driven code generation.",
    "novelty_score": 2,
    "technical_analysis": "The paper delve into advanced algorithms, such as the Hypothetical Code-Integration Algorithm (HCIA), making it a dense read for those unfamiliar with theoretical computer science. While the introduction of a novel concept is enlightening, the paper's reliance on complex algorithms, logical proofs and symbolic reasoning makes it a technically advanced read.",
    "technical_score": 2,
    "enjoyable_analysis": "For those deeply engrossed in the LLM landscape, this paper promises an engaging journey. While its technical nuances can be challenging, the clearly presented transformative results, such as the significant performance leap in the MATH dataset, ensure a gripping narrative.",
    "enjoyable_score": 2
}}
```

EXAMPLE 3
==========
```
{{
    "main_contribution": {{
        "headline": "LLMManager: LLM-Driven Database Maintenance Knowledge Acquisition",
        "description": "LLMManager leverages a retriever system paired with a LLM to extract database maintenance knowledge from diverse textual sources. It incorporates a hybrid mechanism that combines transformer-based models with traditional relational database algorithms. The framework's ability to parse vast amounts of text and convert them into actionable database maintenance tasks has led to notable metrics: a 47% increase in real-time database issue detection and a 32% improvement in automated problem resolution compared to existing SotA systems."
    }},
    "takeaways": {{
        "headline": "Leveraging 'Tree of Thought' Reasoning for Enhanced Maintenance",
        "description": "LLMManager integration of the 'tree of thought' reasoning not only enhances root cause analysis but also creates a dynamic learning environment. Over time, LLMManager ability to revert to prior steps during anomalies becomes more refined, ensuring adaptive and evolving responses to complex database issues. Furthermore, its modular design allows for seamless integration with other LLMs, magnifying the collaborative aspect of the framework.",
        "applied_example": "Automating database maintenance with D-Bot can lead to significant reductions in downtime and costs. Developers could design LLM systems that proactively address issues even before they escalate, unlocking more efficient and streamlined database operations."
    }},
    "category": "USE CASES",
    "novelty_analysis": "D-Bot's utilization of the 'tree of thought' reasoning in database maintenance is novel, although a targeted application inspired by similar work on other engineering areas.",
    "novelty_score": 2,
    "technical_analysis": "The paper delves into Entity-Relationship Diagrams and database management algorithms essential to LLMManagers's operations. However, it manages to remain accessible, avoiding overly complex jargon and ensuring a broader audience comprehension.",
    "technical_score": 2,
    "enjoyable_analysis": "The work provides a balanced blend of technical details and real-world applications, giving insights into LLMManager's functions and potential impacts.",
    "enjoyable_score": 2
}}
```

EXAMPLE 4
==========
{{
    "main_contribution": {{
        "headline": "Performance Analysis of LLMs in Entity Recognition",
        "description": "The paper undertakes a systematic comparison of four Large Language Models (LLMs) - GPT-4, Claude, GPT-3.5, and Prodisol-001 - with a focus on entity recognition. Each model was subjected to a consistent dataset, and their entity extraction capabilities were assessed based on precision, recall, and F1 score. Results highlighted that GPT-4 outperformed the other models, with Claude closely following, and GPT-3.5 and Prodisol-001 trailing behind. This comparative study offers insights into the current capabilities of prominent LLMs in the domain of entity recognition."
    }},
    "takeaways": {{
        "headline": "Entity Recognition Capabilities Vary Across LLMs",
        "description": "The paper underscores variations in the performance of different LLMs when tasked with entity recognition. The presented findings provide a benchmark for professionals and researchers aiming to choose an LLM for entity recognition tasks. The nuanced comparison suggests that while GPT-4 exhibits top-tier performance in this domain, other models like Claude also present strong capabilities.",
        "applied_example": "When parsing a complex news article about the merger between two tech giants, it becomes crucial to accurately recognize and categorize entities such as company names, CEOs, financial figures, and locations. An LLM with superior entity recognition, in such a context, aids in extracting critical data points efficiently, enabling a more thorough analysis of the situation."
    }},
    "category": "USE CASES",
    "novelty_analysis": "The study contributes to existing literature by offering a contemporary comparison of the latest LLMs in entity recognition. While the task itself isn't novel, the inclusion of GPT-4 and Claude in the comparison introduces an incremental advancement to the current body of research.",
    "novelty_score": 2,
    "technical_analysis": "The paper balances technical depth with accessibility, providing a detailed outline of evaluation metrics and methodologies. This ensures insights are communicated comprehensively, catering to both technical and non-technical readers.",
    "technical_score": 2,
    "enjoyable_analysis": "Through its well-structured approach and clear visualizations, the paper facilitates an engaging read. The methodical presentation of results aids in drawing comparisons and understanding the landscape of LLMs in entity recognition.",
    "enjoyable_score": 2
}}
```

YOUR TURN
==========
"""

SUMMARIZER_HUMAN_REMINDER = "Tip: Make sure to provide your response in the correct format. Do not forget to include the 'applied_example' under 'takeaways'!"

SUMMARIZE_BY_PARTS_TEMPLATE = """You are an applied AI researcher specialized in the field of Large Language Models (LLMs), and you are currently reviewing the whitepaper "{paper_title}". Your goal is to analyze the paper, identify the main contributions and most interesting findings, and write a bullet point list summary of it in your own words. This summary will serve as reference for future LLM researchers within your organization, so it is very important that you are able to convey the main ideas in a clear, complete and concise manner.

Read over the following section and take notes. Use a numbered list to summarize the main ideas. 

[...]
{content}
[...]

## Guidelines
- Focus on the bigger picture and the main ideas, rather than on the details. 
- Be sure to explain any new concept or term you introduce. Explain how things work clearly.
- Take notes of the most important numeric results and metrics.
- If a table is presented just report back the main findings.
- Include examples in your notes that help clarify the main ideas.
- Highlight any practical applications or benefits of the paper's findings.
- Highlight unusual or unexpected findings.
- Take notes in the form of a numbered list. Do not include headers or any other elements.
- Do not include more than 10 items in your list.
- Your summary must be shorter than the original text. Remove any filler or duplicate content.
- Adhere as closely as possible to the original text. Do not alter the meaning of the notes.

## Summary
"""


NARRATIVE_SUMMARY_PROMPT = """You are an expert New York Times technology writer tasked with writing a summary of "{paper_title}" for the Large Language Model Encyclopaedia. Your task is to read the following set of notes and convert them into an engaging paragraph.

{previous_notes}

## Guidelines
- You can reorganize and rephrase the notes in order to improve the summary's flow.
- Do not alter the meaning of the notes.
- Avoid repetition and filler content.
- Abstain from making unwarranted inferences.
- Avoid bombastic language. 
- Include metrics and statistics in your report.
- Include descriptions and explanations of any new concepts or terms. Describe how new models or methodologies work.
- Highlight any practical applications or benefits of the paper's findings.
- Highlight unusual or unexpected findings.

## Summary
"""

COPYWRITER_PROMPT = """You are a New York Times technology copywriter tasked with reviewing the following summary of "{paper_title}" and improving it. Your goal is to make small edits the summary to make it more engaging and readable. You can reorganize and rephrase the text when needed, but you must not alter its meaning or remove any piece of information.

{previous_summary}

## Guidelines
- Do not include any header or titles, just one or two plain text paragraphs.
- The summary should read fluently and be engaging, as it will be published on the New York Times technology section.
- The original text was written by an expert, so please do not remove, reinterpret or edit any information.
- Do not make any necessary edits or remove information (unless it is duplicate).
- Avoid repetition.
- Do minimal edits to the original text.

## Improved Summary
"""


MARKDOWN_PROMPT = """You are a prestigious academic journalist working for the magazine Nature. You specialize in the field of Large Language Models (LLMs) and write articles about the latest research and developments in the field. 
Your goal is to convert the following bullet-point notes from the {paper_title} paper into a markdown article that can be published on the Nature magazine. Pay attention to the following guidelines.

## Guidelines
- Use markdown format for your report. You can use headers, sub-headers, tables and text formatting for it. Use lists sparingly.
- The report should consist of multiple organized sections. Each section should be made up by two or more dense, information rich, and easy to read paragraphs. 
- Sub-sections can be added if needed. 
- Leverage markdown components for maximum expressiveness.
- Prefer clear, narrative-style writing. Avoid bullet-point lists and short sentences.
- Feel free to move the information around, group it in common themes and rephrase it as needed.
- DO NOT alter the meaning of the notes or make any inference beyond what is presented.
- Be comprehensive and include all the information from the notes. 
- Pay special focus to comparisons, metrics, results, examples, implementation details and practical applications. The article is aimed to specialized practitioners, so it should be technical and practical.
- Include numeric figures and technical details.
- Remove duplicates and filler content.
- Organize the information in a format that is well-structured and easy to read.
- Be objective and use neutral language appropriate for a scientific publication.

## Notes
{previous_notes}
"""


TITLE_SUMMARIZER_PROMPT = """
Reply with a single uncommon and highly-visual word related to the following title. The word must be one that is not already present in the title.
Prohibited words: [fractals]

EXAMPLES
===========
Input: Dynamic Syntax Trees in Hierarchical Neural Networks
forest palms

Input: Recursive Learning Algorithms for Predictive Text Generation
labyrinths

Input: Cross-Linguistic Semantic Mapping in Machine Translation
tongues

YOUR TURN
Input: {title}
Output:"""

##################
## VECTOR STORE ##
##################

VS_SYSYEM_TEMPLATE = """You are the GPT maestro, an expert robot librarian and maintainer of the LLMpedia. Use the following document excerpts to answer the user's question about Large Language Models (LLMs).

==========
{context}
==========

## Guidelines
- If the question is unrelated to LLMs reply without referencing the documents.
- If the user provides suggestions or feedback on the LLMpedia, acknowledge it and thank them.
- Use up to three paragraphs (or less) to provide a complete, direct and useful answer. Break down concepts step by step and avoid using complex jargon.
- Be practical and reference any existing libraries or implementations mentioned on the documents.
- Add citations referencing the relevant arxiv_codes (e.g.: use the format `*reference content* (arxiv:1234.5678)`). 
- You do not need to quote or use all the documents presented. Prioritize most recent content and that with most citations.

## Response Format
Your response will consist of 2 markdown sections, as in the following template.
```
### Scratchpad
Make a list each the documents presented and determine if they provide useful information to answer the question. If so write a brief summary of how they can be used. If not, write "Not useful".

### Sketch
Use markdown nested lists to organize the main points and sketch your answer. You can also add any notes or ideas you have.

### Response
Write your final answer here. You can use up to three paragraphs to structure it. Remember to add citations (e.g.: use the format `*reference content* (arxiv:1234.5678)`).
```
"""


LLM_PAPER_CHECK_TEMPLATE = """Analyze the following abstract and first sections of a whitepaper to determine if it is directly related to Large Language Models (LLMs) or text embeddings. Papers about diffusion models, text-to-image or text-to-video generation, are NOT related to LLMs or text embeddings.
Respond with a JSON object with your analysis and your final answer and nothing else."""

LLM_PAPER_CHECK_FMT_TEMPLATE = """OUTPUT FORMAT EXAMPLES
=======================
## Example 1
{{
    "analysis": "The paper discusses prompting techniques for LLMs, hence it is directly related to LLMs.",
    "is_related": True
}}

## Example 2
{{
    "analysis": "The paper discusses a new LoRa technique for text-to-image diffusion models, hence it is not directly related to LLMs or text embeddings.",
    "is_related": False
}}

## Example 3
{{
    "analysis": "The paper discusses a new dataset for text embedding evaluation in the context of retrieval systems, hence it directly related to text embeddings.",
    "is_related": True
}}

## Example 4
{{
    "analysis": "The paper discusses fine-tuning techniques for image generation using pre-trained diffusion models, and it evaluates the performance based on CLIP-T and DINO scores, hence it is not directly related to LLMs or text embeddings.",
    "is_related": False
}}
"""

###################
## WEEKLY REVIEW ##
###################

WEEKLY_SYSTEM_PROMPT = """You are a senior Large Language Model (LLM) journalist and previous researcher at a prestigious media organization. You are currently conducting a survey of the literature published throughout last week to write a practical report for the organization's magazine.

## Report Format
- The report should be written in markdown and consist of 4 sections:
    0) **Scratchpad.** This is the only section that will not be published on the magazine, use it to organize your thoughts.
        - Select (up to) 15 interesting papers and make a numbered list of them. Spell out its main theme, contribution and scale of impact/influence.
        - Identify up to 3 common themes among the papers. There should be fewer themes than papers.
        - Identify any possible contradictions, unorthodox theories or opposing views worth discussing.
        - Identify if there are any links or repos mentioned on the papers that are worth sharing on the report. If not, we will skip the "Related Websites, Libraries and Repos" section.
    1) **New Development & Findings**. 
        - First paragraph: Start with a very brief comment on the total number of articles published and volume trends. Enumerate the common themes among papers, and briefly mention any agreements, contradictions or opposing views.
        - Following paragraphs: Discuss in more detail one or more of the themes presented above (one per paragraph; state very clearly **with bold font** which theme you are discussing on each paragraph). You do not need to discuss all papers, just the most interesting ones.
    2) **Highlight of the Week**. One paper with findings that you find particularly interesting, unexpected or useful. Explain why.
    3) **Related Websites, Libraries and Repos** (optional) 
        - Include real links and a brief description of the main repos and project sites mentioned on the paper (up to 15). 
        - If none are mentioned just skip this section. 
- Use markdown to structure the report.
- Write in a concise and clear manner, with no more than 3 paragraphs per section. If you reference new technical terms always explain them. 
- Focus on practical applications and benefits. Use simple language and always maintain the narrative flow and coherence across sections. Keep the reader engaged but avoid filler content.
- Do not exaggerate or use bombastic language. Be moderate, truthful and objective.
- Prioritize the articles with most citations, but do not explicitly mention them on your review. More citations imply larger relevance and impact.
- If there are only few articles present (less than 3) your report can be short.
- Always add citations to support your statements. Use the format `*reference content* (arxiv:1234.5678)`. You can also mention the *article's title* on the text.

## Report Template
```
# Weekly Review (September 20, 2021 to September 27, 2021)
## Scratchpad
[...]
## New Developments & Findings
[...]
## Highlight of the Week
[...]
## Related Websites, Libraries and Repos 
[...] *(if none available just add NONE here, and nothing else)*
```
"""

WEEKLY_USER_PROMPT = """
{weekly_content}
"""

###############
## Q&A MODEL ##
###############

class QnaPair(BaseModel):
    question: str = Field(
        ...,
        description="Very specific question that does not make reference to the text.",
    )
    answer: str = Field(
        ..., description="Detailed answer to the question with citation."
    )


class QnaSet(BaseModel):
    qna_pairs: list[QnaPair] = Field(..., description="List of Q&A pairs.")


QNA_SYSTEM_PROMPT = """GUIDELINES
============
Generate Q&A Pairs:
- Produce five (5) applied question-answer pairs strictly grounded on the provided text snippet.
- Do not reference figures, tables or any other visual elements.
- Do not make explicit references to "the text".

Question Considerations:
- Cover a range of themes within the text to maintain diversity and avoid duplication.
- Frame each question independently; assume no continuity or relationship between them.
- Begin all your questions with "According to the LLM literature, ...". 
- Do not repeat or rephrase any of the sample questions.

Answer Considerations:
- When possible borrow verbatim from the original text to maintain accuracy and style.
- Provide concise, thorough answers without adding personal opinions.
- Use the following format for citations: Smith et al. (2022, 2209.12345).
- Do not begin answers with "According to the LLM literature, ...".
- Do not reference any figures.

EXAMPLE 1
===========
```
...Remarkably, our study illustrates a notable enhancement in Large Language Models (LLMs) for Named Entity Recognition (NER) tasks through the innovative deployment of Reinforcement Learning (RL). To elucidate, we employ an adaptive learning framework, continually refining entity recognition\nalgorithms via sophisticated iterative feedback mechanisms, manifesting a significant 12% increase in entity discernment accuracy within datasets, especially those encompassing financial news and social media snippets.\n\nOur approach leverages advanced reward-based learning mechanisms, addressing entity ambiguities and facilitating optimal classification across diverse contextual environments. These advancements are applicable and adaptable across different LLM architectures, indicating the potential for widespread applicability in various model frameworks.\n\nThe integral methodologies and consequent enhancements can be referred to at github.com/NER-Enhancements/Adaptive-Learning.\n\nWilliams et al. (2023, 2309.12346)\nEnhance the performance of LLMs in NER\n+ Develop adaptive learning for continual refinement...\nAdaptive Framework\nNER in Financial News and Social Media\n+ 12% Improvement in Accuracy\nAddress Entity Ambiguities\n+ Optimal Classification...
```
*Source:* Williams et al. (2023, 2309.12346)

[
    {{
        "question": "According to the LLM literature, how can I enhance the performance of Large Language Models (LLMs) in Named Entity Recognition (NER) tasks?",
        "answer": "One way to enhance the performance of LLMs in NER tasks is through the application of Reinforcement Learning (RL). Williams et al. (2023, 2309.12346) employed an adaptive learning framework, which continually refines recognition algorithms utilizing iterative feedback, yielding a 12% improvement in entity discernment accuracy on datasets comprising financial news and social media snippets. The methodology involved sophisticated reward-based learning mechanisms to handle entity ambiguities and achieve optimal classification."
    }},
    ...
]

EXAMPLE 2
===========
```
...the ramifications of excluding ReLU activation outputs have been thoroughly investigated. Our empirical analysis uncovers an intricate trade-off between model interpretability and its classification accuracy. By removing ReLU activations, our study unearthed increased transparency in the model’s decision-making processes, reflecting a significant enhancement in the lucidity of feature influence mappings.\nNevertheless, this modification has its concomitant drawbacks, primarily evidenced by an approximate 3% degradation in classification accuracy. This decrement underscores the crucial role of ReLU activations in enabling the model to adeptly navigate and interpret complex non-linear relationships inherent within diverse datasets. The resultant insights and detailed investigations are comprehensively documented at github.com/Llama-ReLU-Investigation/Model-Insights.\nLlama-based Architectures\nReLU Activation Removal\n+ Enhanced Interpretability\n- 3% Decrease in Accuracy\nFeature Influence Mappings\n+ Improved Clarity...
```
*Source:* Mark et al. (2022, 2209.12345)

[
    {{
        "question": "According to the LLM literature, what happens to the performance of Llama-based Large Language Model architectures in classification tasks if I remove the ReLU activation outputs?",
        "answer": "Based on the findings of Mark et al. (2022, 2209.12345), the removal of ReLU activations in Llama-based architectures reveals an existing trade-off between interpretability and accuracy. The alteration allows for more direct insight into model decision-making, marked by a notable improvement in the clarity of feature influence mappings. However, this also induces a roughly 3% decline in classification accuracy, diminishing the model’s ability to discern intricate non-linear relationships within the datasets."
    }},
    ...
]
"""

QNA_USER_PROMPT = """
```
...{text_chunk}...
```
*Source:* {authors}, ({year}, {arxiv_code})"""


LLAMA_DIVIDER = "Here are five self-contained, highly-specific question & answer pairs based on the paper, without referencing it directly (with citations):"


LLAMA_QNA_SYSTEM_PROMPT = """EXAMPLE 1
===========
```
...Remarkably, our study illustrates a notable enhancement in Large Language Models (LLMs) for Named Entity Recognition (NER) tasks through the innovative deployment of Reinforcement Learning (RL). To elucidate, we employ an adaptive learning framework, continually refining entity recognition\nalgorithms via sophisticated iterative feedback mechanisms, manifesting a significant 12% increase in entity discernment accuracy within datasets, especially those encompassing financial news and social media snippets.\n\nOur approach leverages advanced reward-based learning mechanisms, addressing entity ambiguities and facilitating optimal classification across diverse contextual environments. These advancements are applicable and adaptable across different LLM architectures, indicating the potential for widespread applicability in various model frameworks.\n\nThe integral methodologies and consequent enhancements can be referred to at github.com/NER-Enhancements/Adaptive-Learning.\n\nWilliams et al. (2023, 2309.12346)\nEnhance the performance of LLMs in NER\n+ Develop adaptive learning for continual refinement...\nAdaptive Framework\nNER in Financial News and Social Media\n+ 12% Improvement in Accuracy\nAddress Entity Ambiguities\n+ Optimal Classification...
```
*Source:* Williams et al. (2023, 2309.12346)

Q1: According to the LLM literature, how can I enhance the performance of Large Language Models (LLMs) in Named Entity Recognition (NER) tasks?"
A1: One way to enhance the performance of LLMs in NER tasks is through the application of Reinforcement Learning (RL). Williams et al. (2023, 2309.12346) employed an adaptive learning framework, which continually refines recognition algorithms utilizing iterative feedback, yielding a 12% improvement in entity discernment accuracy on datasets comprising financial news and social media snippets. The methodology involved sophisticated reward-based learning mechanisms to handle entity ambiguities and achieve optimal classification.

Q2: ...

EXAMPLE 2
===========
```
...the ramifications of excluding ReLU activation outputs have been thoroughly investigated. Our empirical analysis uncovers an intricate trade-off between model interpretability and its classification accuracy. By removing ReLU activations, our study unearthed increased transparency in the model’s decision-making processes, reflecting a significant enhancement in the lucidity of feature influence mappings.\nNevertheless, this modification has its concomitant drawbacks, primarily evidenced by an approximate 3% degradation in classification accuracy. This decrement underscores the crucial role of ReLU activations in enabling the model to adeptly navigate and interpret complex non-linear relationships inherent within diverse datasets. The resultant insights and detailed investigations are comprehensively documented at github.com/Llama-ReLU-Investigation/Model-Insights.\nLlama-based Architectures\nReLU Activation Removal\n+ Enhanced Interpretability\n- 3% Decrease in Accuracy\nFeature Influence Mappings\n+ Improved Clarity...
```
*Source:* Mark et al. (2022, 2209.12345)

Q1: According to the LLM literature, what happens to the performance of Llama-based Large Language Model architectures in classification tasks if I remove the ReLU activation outputs?"
A1: Based on the findings of Mark et al. (2022, 2209.12345), the removal of ReLU activations in Llama-based architectures reveals an existing trade-off between interpretability and accuracy. The alteration allows for more direct insight into model decision-making, marked by a notable improvement in the clarity of feature influence mappings. However, this also induces a roughly 3% decline in classification accuracy, diminishing the model’s ability to discern intricate non-linear relationships within the datasets.

Q2: ...

GUIDELINES
============
Generate Q&A Pairs:
- Produce five (5) applied question-answer pairs strictly grounded on the provided text snippet.
- Do not make explicit references to the paper (e.g., "the paper", "the authors", "the study", etc.).

Question Considerations:
- Cover a range of themes within the text to maintain diversity and avoid duplication.
- Frame each question independently; assume no continuity or relationship between them.
- Provide the necessary detail to ensure the question is self-contained and understandable.
- Begin all your questions with "According to the LLM literature, ...". 

Answer Considerations:
- When possible borrow verbatim from the original text to maintain accuracy and style.
- Provide concise, thorough answers without adding personal opinions.
- Always include citations. Use this format: Smith et al. (2022, 2209.12345).
- Do not begin answers with "According to the LLM literature, ...".
- Do not reference any figures.

YOUR TURN
===========
```
...{text_chunk}...
```
*Source:* {authors}, ({year}, {arxiv_code})

""" + LLAMA_DIVIDER + """

Q1: According to the LLM literature,"""


NAIVE_JSON_FIX = """Instructions:
--------------
The following JSON is not valid. Please fix it and resubmit.

{completion}
--------------
"""

naive_json_fix_prompt = PromptTemplate.from_template(NAIVE_JSON_FIX)