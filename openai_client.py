#!/usr/bin/env python3
"""
DOGMA 24/7 - OpenAI Client
Integración con GPT-4 y otros modelos de OpenAI
"""
import os
from openai import OpenAI
from typing import Optional, List, Dict

class DogmaOpenAIClient:
    """Cliente de OpenAI para DOGMA 24/7"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.org_id = os.getenv('OPENAI_ORG_ID')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', 4096))
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY no configurada")
        
        self.client = OpenAI(
            api_key=self.api_key,
            organization=self.org_id
        )
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generar respuesta con GPT"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens or self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error en chat completion: {e}")
    
    def generate_ad_copy(
        self,
        product: str,
        target_audience: str,
        tone: str = "profesional"
    ) -> Dict[str, str]:
        """Generar copy para anuncios"""
        prompt = f"""
        Genera copy para un anuncio de Meta Ads:
        
        Producto: {product}
        Audiencia: {target_audience}
        Tono: {tone}
        
        Proporciona:
        1. Título (25 caracteres max)
        2. Descripción principal (90 caracteres max)
        3. Call to action
        4. 3 variaciones del copy
        """
        
        content = self.chat_completion([
            {"role": "system", "content": "Eres un copywriter experto en anuncios digitales."},
            {"role": "user", "content": prompt}
        ])
        
        return {"generated_copy": content}

def get_openai_client() -> DogmaOpenAIClient:
    """Obtener instancia del cliente OpenAI"""
    return DogmaOpenAIClient()
