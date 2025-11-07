import re

def clean_text(text: str) -> str:
    """This function is mainly for cleaning user input to improve token usage and relevance for the model
    :param text: Text you would like to clean
    :return : The text after its been cleaned
    """
    
    #remove any weird non ASCII text
    text = text.encode(encoding='ascii', errors='ignore').decode()
    
    #multiple punctuation
    text = re.sub(r'!+', '!', text)
    #extra whitespaces
    text = re.sub(r'[ \t]+', ' ', text)
    #paragaph breaks
    text = re.sub(r'\n\s+\n', '\n\n', text)
    #multiple commas
    text = re.sub(r'[,]+', ',', text)
    #multiple periods
    text = re.sub(r'[.]+', '.', text)    
    
    return text.strip()