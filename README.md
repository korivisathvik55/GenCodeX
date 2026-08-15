\# GenCodeX



GenCodeX is an AI-powered GitHub codebase assistant that uses Retrieval-Augmented Generation (RAG) to understand and explain source code.



It retrieves source code from GitHub, splits the code into chunks, creates semantic embeddings, searches the most relevant code using FAISS, and generates an explanation using a locally running Qwen2.5-Coder model through Ollama.



\## Features



\- GitHub repository integration

\- Source-code retrieval

\- Code chunking

\- Semantic code embeddings

\- FAISS vector similarity search

\- Retrieval-Augmented Generation (RAG)

\- Local LLM inference using Ollama

\- Qwen2.5-Coder 3B

\- FastAPI backend

\- React + Vite frontend

\- Retrieved source-code display

\- Markdown-formatted AI responses

\- API error handling

\- CORS support for frontend-backend communication



\## Architecture



```text

&#x20;                   GenCodeX

&#x20;                      |

&#x20;                      v

&#x20;             React + Vite Frontend

&#x20;                      |

&#x20;                      v

&#x20;               FastAPI Backend

&#x20;                      |

&#x20;            +---------+---------+

&#x20;            |                   |

&#x20;            v                   v

&#x20;       GitHub Service      Code Processing

&#x20;                                |

&#x20;                                v

&#x20;                          Code Chunking

&#x20;                                |

&#x20;                                v

&#x20;                          Embeddings

&#x20;                                |

&#x20;                                v

&#x20;                          FAISS Search

&#x20;                                |

&#x20;                                v

&#x20;                      Relevant Code Context

&#x20;                                |

&#x20;                                v

&#x20;                        Ollama / Qwen2.5

&#x20;                                |

&#x20;                                v

&#x20;                        Generated Answer

&#x20;                                |

&#x20;                                v

&#x20;                        React Frontend

