import hashlib
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from the .env file")



doc_text = """
Suraj Jena is a software engineer and full-stack developer from Odisha, India. He completed his Bachelor of Technology in Computer Science and Engineering from Trident Academy of Technology, Bhubaneswar, graduating with a CGPA of approximately 7.75. Throughout his engineering journey, Suraj developed a strong interest in software engineering, backend development, cloud technologies, distributed systems, artificial intelligence, and scalable web applications.

Suraj currently works at Actify Business as a Junior Software Engineer after initially joining as an intern. During his time at Actify, he has contributed to CRM portals, CMS platforms, SEO improvements, reusable UI components, dynamic form builders, performance optimization, and various production-level business applications. His day-to-day work primarily revolves around React, Next.js, TypeScript, Redux Toolkit, React Hook Form, Zod, Tailwind CSS, API integration, and modern frontend architecture. Besides frontend development, he continuously studies backend engineering independently to become a complete full-stack developer.

His backend technology stack includes Node.js, Express.js, FastAPI, REST APIs, authentication using JWT, cookies, middleware, role-based authorization, PostgreSQL, MySQL, MongoDB, Prisma ORM, SQL optimization, migrations, API design, pagination, file uploads, AWS concepts, Azure concepts, and cloud deployment. He enjoys understanding how backend systems actually work instead of simply memorizing frameworks. His learning approach focuses heavily on implementation and production architecture rather than theory alone.

Suraj has also been deeply exploring Generative AI engineering. His AI stack includes LangChain, LangGraph, Retrieval Augmented Generation (RAG), vector databases, PGVector, embeddings, OpenAI models, HuggingFace embeddings, MCP servers, tool calling, supervisor agents, ReAct agents, multi-agent systems, document loaders, text splitting strategies, retrieval pipelines, and production AI workflows. He believes AI should accelerate software development but not replace the engineer's understanding of system design and business logic.

One of Suraj's major AI projects is Explora.ai, an intelligent travel planning application that uses multiple AI agents including Planner, Searcher, and Summarizer agents. The application integrates weather information, search APIs, PDF retrieval, itinerary generation, and Retrieval Augmented Generation pipelines to provide personalized travel recommendations. The project combines LangGraph orchestration, FastAPI backend services, PostgreSQL storage, vector databases, and React-based frontend applications.

Another important project is CareSync, a hospital management platform designed to streamline hospital operations. The application includes centralized administration, patient management, appointment booking, report management, AI-powered health tracking, and intelligent document retrieval using LangGraph and Retrieval Augmented Generation. The system demonstrates Suraj's ability to combine traditional software engineering with modern AI capabilities.

Suraj has also developed MediumX, an AI-powered blogging platform inspired by Medium. The platform includes authentication, blogging features, content management, AI integration, modern frontend architecture, and backend APIs. Apart from this, he has built teacher attendance systems, hospital management systems, news applications using Redux, Todo Manager applications, portfolio websites, dynamic CMS portals, CRM solutions, and several production-ready internal business applications.

His frontend expertise includes React.js, Next.js App Router, React Native, Redux Toolkit, TanStack Query, Tailwind CSS, Shadcn UI, Framer Motion, React Hook Form, Zod validation, Axios, component architecture, responsive design, reusable component systems, SEO optimization, metadata generation, sitemap generation, dynamic routing, authentication flows, and production deployment using Vercel.

His backend expertise includes Express.js, FastAPI, PostgreSQL, MySQL, MongoDB, Prisma ORM, SQL queries, authentication systems, middleware architecture, role-based authorization, file uploads, pagination, API versioning, RESTful architecture, Docker basics, GitHub Actions, testing with Jest, and cloud deployment concepts.

Suraj has also been studying Linux system administration and DevOps fundamentals. His learning includes Ubuntu, WSL, systemd services, process management, networking fundamentals, TCP/IP, HTTP, HTTPS, DNS, WebSockets, Linux commands, Nginx, EC2 deployment, cloud virtual machines, AWS services, Azure services, storage systems, object storage, relational databases, reverse proxies, VPS hosting, and production deployment strategies. He believes understanding infrastructure makes engineers significantly stronger.

Apart from web development, Suraj has a growing interest in React Native mobile application development. He has been learning Expo Router, mobile navigation, native components, Android emulators, mobile deployment, Play Store publishing, and the similarities between React and React Native. He intends to become a developer capable of building web, backend, AI, and mobile applications using a unified JavaScript and TypeScript ecosystem.

Suraj strongly prefers learning by building real-world applications rather than watching endless tutorials. Whenever learning a new technology, he attempts to understand how it actually works internally before relying on third-party libraries. He enjoys low-level programming concepts and has expressed interest in learning C++, operating systems, browser architecture, rendering engines, databases, networking internals, and distributed systems in the future.

He values clean architecture, reusable code, maintainability, SOLID principles, practical software engineering, production-ready systems, and scalable application design. Rather than memorizing interview questions, he prefers understanding why technologies behave the way they do. His curiosity often leads him into exploring how JWT authentication works internally, how cloud services communicate, how vector databases store embeddings, how retrieval pipelines function, how ORMs translate queries into SQL, and how production systems are deployed.

Suraj's long-term career goal is to become an exceptional Full Stack Engineer with deep expertise in Backend Engineering, Artificial Intelligence, Agentic AI Systems, Cloud Infrastructure, Distributed Systems, and Production Software Architecture. He aims to contribute to challenging engineering problems involving scalable APIs, intelligent automation, AI agents, Retrieval Augmented Generation, and cloud-native applications while continuously improving his technical depth across the complete software engineering stack.
"""

document = Document(
    page_content=doc_text,
    metadata={
        "source": "in-memory-doc"
    }
)

text_splitter = RecursiveCharacterTextSplitter( chunk_size=500, chunk_overlap=50)
docs_split = text_splitter.split_documents([document])

primary_id = 1
for doc in docs_split:
    doc.metadata["id"] = primary_id
    primary_id += 1 

embeddings = HuggingFaceEmbeddings( model_name="sentence-transformers/all-mpnet-base-v2" )


vector_store = PGVector(
    embeddings=embeddings,
    collection_name="my_textbase",
    connection=DATABASE_URL,
    use_jsonb=True,
)



vector_store.add_documents( #when we pass ids, we are saying these has to be the PK, otherwise many times chunks gets loaded and tuple gets exceeded always, now only id's gets replaced only not added more .
    documents=docs_split,
    ids= [doc.metadata["id"]  for doc in docs_split])