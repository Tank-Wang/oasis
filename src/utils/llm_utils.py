import openai
from openai import OpenAI
from typing import Optional
import os
from dotenv import load_dotenv

class LLMModel:
    """Wrapper class for LLM model, providing a unified interface"""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        
    def generate(self, prompt: str) -> str:
        """
        Generate LLM response
        
        Args:
            prompt: Input prompt
            
        Returns:
            response: LLM response text
        """
        # TODO: Implement specific LLM call logic
        pass

class GPT(LLMModel):
    """Implementation class for OpenAI GPT model"""
    
    def __init__(self, model_name: str = "gpt-4o-mini", api_key: Optional[str] = None):
        """
        Initialize GPT model
        
        Args:
            model_name: Model name, default is "gpt-4o-mini"
            api_key: OpenAI API key, if None, get from environment variable
        """
        # Load environment variables
        load_dotenv()
        
        # If api_key is not provided, get from environment variable
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')

        super().__init__(model_name, api_key)
        if api_key:
            self.client = OpenAI(api_key=api_key)
            
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: Optional[float] = 0.8, json_mode: Optional[bool] = False) -> str:
        """
        Generate response using OpenAI API
        
        Args:
            prompt: Input prompt
            
        Returns:
            str: GPT response text
        
        Raises:
            Exception: Exception raised when API call fails
        """
        message = [{"role": "user", "content": prompt}]
        if system_prompt:
            message.insert(0, {"role": "system", "content": system_prompt})
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=message,
                temperature=temperature,
                response_format={"type": "json_object"} if json_mode else None
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error in GPT generate: {str(e)}")

if __name__ == "__main__":
    gpt = GPT()
    print(gpt.generate("hello world!"))
