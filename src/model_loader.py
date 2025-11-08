"""This module is meant for loading the model and tokenizer into memory"""
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import logging

model_name_qwen = 'Qwen/Qwen3-4B-Thinking-2507'
model_name_mistral = 'mistralai/Mistral-7B-Instruct-v0.3'


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

#bnb config to run safely on 6GB of GPU VRAM
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)


class ModelLoader:
    
    def __init__(self, model_name: str) -> None:
        """Load the model and tokenizer into memory using model_name. Model must be installed before use
        :param model_name: The name of the model directly from huggingface
        """
        self.model_name = model_name
        self.messages = []
        try:
            self.model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config, dtype='auto', device_map='auto', local_files_only=True)
            logger.info('Model loaded successfully')
        except Exception:
            logger.error('Failed to load model', exc_info=True)
            raise
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            logger.info('Tokenizer loaded successfully')
        except Exception:
            logger.error('Failed to load model', exc_info=True)
            raise

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        logger.info(f'Model: {self.model_name}')
        logger.info(f'Device: {self.device}')
    
    def load_model(self, model_name: str) -> None:
        """Load a new model and tokenizer into memory
        :param model_name: The name of the model directly from huggingface
        """
        self.model_name = model_name
        logger.info(f'Beginning to load new model: {model_name}')
        
        try:
            self.model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config, dtype='auto', device_map='auto',  local_files_only=True)
            logger.info('Model loaded successfully')
        except Exception:
            logger.error('Failed to load model', exc_info=True)
            raise
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            logger.info('Tokenizer loaded successfully')
        except Exception:
            logger.error('Failed to load model', exc_info=True)
            raise
        
        logger.info(f'New model loaded: {model_name}')
    
    def generate(self, prompt: str, max_new_tokens: int = 120, temperature: float = 0.7) -> str:
        """Function for generating a response
        :param prompt: The prompt you would like to ask the model
        :param max_new_tokens: The maximum number of reply tokens you would like to provide
        :param temperature: The temperature of the responses you would like
        :return : A string containing the reply
        """
        self.messages.append({'role': 'user', 'content': prompt})
        prompt = self.tokenizer.apply_chat_template(self.messages,
                                                    tokenize=False,
                                                    add_generation_prompt=True,
                                                    )
        inputs = self.tokenizer(prompt, return_tensors='pt').to(self.device)
        with torch.inference_mode():
            outputs = self.model.generate(**inputs, 
                                        max_new_tokens=max_new_tokens, 
                                        temperature=temperature, 
                                        do_sample=True,
                                        eos_token_id=self.tokenizer.eos_token_id,
                                        pad_token_id=self.tokenizer.pad_token_id,
                                        top_p=0.95,
                                        top_k=20,
                                        repetition_penalty=1.1
                                        )
        text = self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
        self.messages.append({'role': 'assistant', 'content': text})
        logger.info('Prompt reply generated')
        return text
    
    def summary(self) -> None:
        """A summary of the model and the device"""
        print(f'Model name: {self.model_name}')
        print(f'Device: {self.device}')
        if torch.cuda.is_available():
            num_gpus = torch.cuda.device_count()
            print(f"Number of GPUs: {num_gpus}")
            for i in range(num_gpus):
                print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        else:
            print("No CUDA GPU detected, using CPU")
            

#Below is for testing purposes
if __name__ == '__main__':
    model = ModelLoader(model_name_mistral)

    while True:
        inp = input('question: ')

        print(model.generate(inp,max_new_tokens=1000, temperature=0.7))