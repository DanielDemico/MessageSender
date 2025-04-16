from pydantic import BaseModel, Field
from typing import Optional
from groq import Groq
from datetime import datetime



GROQ_API_KEY = "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"
class ResumoRequest(BaseModel):
    conteudo: str = Field(..., description="informações do Lead que serão otimizadas")
    modelo: str = Field("gemma2-9b-it", description="Modelo llm a ser usado")
    temperatura: float = Field(0.7, ge=0, le=1, description="Criatividade do Modelo (0-1)")
    max_tokens: int = Field(300, ge=50, le=1000, description="Tamanho maximo do resumo")
    estilo: Optional[str] = Field("pontos-chave", description="Estilo do Resumo")
    
class AgentResumo:
    def __init__(self):
        self.historico = []
    
    def gerar_resumo(self, request: ResumoRequest) -> str:
        """Gera um resumo com os pontos principais do Lead Fornecido"""
        
        prompt = f"""
        Por favor, crie um resumo do cliente,
        usando essas informações: {request.conteudo}
        
        Regras: 
        - Pegue as informações importantes do cliente
        - Mantenha fidelidade ao conteudo
        - Destaque informações uteis sobre o cliente
        """
        
        try: 
            client = Groq(
                api_key=GROQ_API_KEY,
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=request.modelo,
                temperature=request.temperatura
            )
            resumo = chat_completion.choices[0].message.content
            return resumo
        except Exception as e:
            raise ValueError(f"Erro ao tentar gerar o resumo: {e}")
        
        def _registrar_historico(self,request: ResumoRequest,resumo:str):
            """Registra a operação no histórico"""
            self.historico.append({
                "request":request.dict(),
                "resumo": resumo,
                "timestamp":datetime.now().isoformat()
            })
        def obter_historico(self) -> list:
            """Retorna o historico de resumos gerados"""
            return self.historico
    


def make_resume_agent(tavily_resum):
    content = tavily_resum
    agente = AgentResumo()
    
    request = ResumoRequest(
        conteudo = content,
        modelo = "gemma2-9b-it",
        temperatura=0.5,
        max_tokens=1000,
        estilo="N"
    )
    try: 
        resumo = agente.gerar_resumo(request)

    except Exception as e:
        print(f"erro: {e}")

