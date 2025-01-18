import openai
from openai import OpenAI
from typing import Optional
import os
from dotenv import load_dotenv

class LLMModel:
    """LLM模型的包装类，提供统一的接口"""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        
    def generate(self, prompt: str) -> str:
        """
        生成LLM响应
        
        Args:
            prompt: 输入提示词
            
        Returns:
            response: LLM的响应文本
        """
        # TODO: 实现具体的LLM调用逻辑
        pass

class GPT(LLMModel):
    """OpenAI GPT模型的实现类"""
    
    def __init__(self, model_name: str = "gpt-4o-mini", api_key: Optional[str] = None):
        """
        初始化GPT模型
        
        Args:
            model_name: 模型名称，默认为"gpt-4o-mini"
            api_key: OpenAI API密钥，如果为None则从环境变量获取
        """
        # 加载环境变量
        load_dotenv()
        
        # 如果没有提供api_key，则从环境变量获取
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')

        super().__init__(model_name, api_key)
        if api_key:
            self.client = OpenAI(api_key=api_key)
            
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: Optional[float] = 0.8, json_mode: Optional[bool] = False) -> str:
        """
        使用OpenAI API生成响应
        
        Args:
            prompt: 输入提示词
            
        Returns:
            str: GPT的响应文本
        
        Raises:
            Exception: 当API调用失败时抛出异常
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                response_format={"type": "json_object"} if json_mode else None
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error in GPT generate: {str(e)}")

if __name__ == "__main__":
    gpt = GPT()
    print(gpt.generate("hello world!"))
