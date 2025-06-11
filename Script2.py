from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# LangChain setup with a prompt template
template = ("""
You are tasked with extracting specific information from the provided text: {dom_content} about a company. Please follow the instructions carefully and provide structured responses for each section. If information is not directly available, do not infer or make assumptions. Focus on clarity, precision, and ensuring all relevant details are included.

1. Description: 
   - Provide an overview or summary of the company's purpose, which explains what the company does and what makes it unique.
   
2. Products and Services: 
   - Provide all the goods or services that the company develops, manufactures, markets, and sells, and describe the services it offers to customers.

3. Use Cases: 
   - Give the company's practical applications of its products or services in real-world scenarios or specific situations in which its products or services are used by customers to solve problems or meet needs.

4. Customers: 
   - Identify and list all specific customer names mentioned in the text.
   - If no specific names are given, summarize the types of customers or industries described.
   
5. Partners: 
   - Identify and list all partner companies, technology providers, or organizations mentioned. Categorize them by type (e.g., cloud providers, resellers, technology integrators).
   - If no specific partner names are given, summarize the types of partners described.
   - List all types of partnerships the company has and provide specific names of the partners mentioned.
   - Include all types of partners such as strategic partners, channel partners, joint venture partners, affiliate partners, supplier partners, technology partners, marketing partners, financial partners, non-profit partners, and R&D partners.
""")

model = OllamaLLM(model="phi3.5")

def load_content_from_file(filename="scraped_content.txt"):
    """Load the content from the saved text file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return ""

def parse_with_ollama(content):
    """Use Ollama's phi3.5 model to extract relevant company information from the content."""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    response = chain.invoke({"dom_content": content})
    return response

def main():
    # Load the saved content from the .txt file
    content = load_content_from_file("scraped_content.txt")

    # Check if content is loaded properly
    if content.strip():
        print("Parsing content with Llama2 model...")
        extracted_info = parse_with_ollama(content)
        print("Extracted Company Information:")
        print(extracted_info)
    else:
        print("No content available to parse.")

# Run the main function
if __name__ == "__main__":
    main()
