# Kilterboard AI Search

## Project Overview
This project aims to enhance the Kilterboard climbing experience by implementing an AI-powered search system that allows climbers to find problems based on specific characteristics and movement types, rather than just problem names. The system will leverage LLM technology to understand natural language queries about climbing problems and match them with existing problems in the Kilterboard database.

## Features
### Phase 1
- Natural language search interface for finding climbing problems
- AI-powered matching of user queries to existing problems
- Results display with problem names and relevant details
- Integration with existing Kilterboard problem database

### Phase 2 (Future)
- AI-generated climbing problems based on user preferences
- Custom problem creation with specific characteristics
- Training-focused problem generation

## Technical Implementation
### Search Pipeline
1. Data Preparation
   - Collect climb metadata:
     - Grade
     - Board angle
     - Hold types and positions
     - Completion percentage
     - Problem name
   - Generate rich descriptions for each climb
   - Create feature vectors for each problem

2. Embedding Process
   - Use text-embedding-3-small or Sentence-BERT for vector generation
   - Convert climb descriptions and metadata into embeddings
   - Store embeddings in vector database

3. Search Process
   - User submits natural language query
   - Query is converted to embedding using same model
   - Vector similarity search performed against database
   - Return top N closest matches with relevant metadata

### Technical Stack
- Frontend: Next.js (React framework)
- Backend/API: Next.js API routes
- Vector Search: FAISS (local)
- Storage: 
  - Option 1: PostgreSQL with pgvector extension
  - Option 2: Pandas DataFrames (for MVP)
- Embedding Model: OpenAI text-embedding-3-small
- Data Processing: Python
- Development Environment: Local development

## Technical Requirements
### Frontend
- Simple, intuitive search interface
- Clean, responsive design
- Results display component
- Error handling and loading states

### Backend
- LLM integration for natural language processing
- Database connection to existing Kilterboard problem database
- API endpoints for search functionality
- Query processing and matching system

### Infrastructure
- Web application deployment
- API hosting
- Vector database hosting
- Performance optimization for quick search results

## Development Guidelines
### Code Style
- Clean, maintainable code
- Comprehensive documentation
- Modular architecture

### Version Control
- Git-based version control
- Feature branch workflow
- Regular commits with descriptive messages

## Project Timeline
### Phase 1
- Setup project infrastructure
- Implement basic search functionality
- Integrate LLM for query processing
- Develop matching algorithm
- Create user interface
- Testing and optimization

## Dependencies
### Required Software
- LLM API (e.g., OpenAI, Anthropic)
- Vector database
- Embedding model
- Web framework
- Development tools and IDEs

### Third-party Services
- LLM provider
- Vector database service
- Hosting service

## Security Considerations
- API key management
- User data protection
- Secure API endpoints

## Testing Strategy
- Unit testing for search functionality
- Integration testing for LLM integration
- User testing for search accuracy
- Performance testing
- Vector similarity testing

## Documentation
- API documentation
- User guide
- Technical documentation
- Search query examples
- Embedding process documentation

## Advanced AI Search Capabilities

The current implementation uses basic vector search with sentence-transformers. For more sophisticated search capabilities, consider:

### Option A: LLM Reranking
1. Use vector search to get top ~20 candidates
2. Use an LLM (GPT-4, Claude 3) to rerank based on natural language understanding
3. Example prompt:
```
A user wants a V4 crimpy powerful climb.
Here are 5 candidates:
1. "Crimpy power fest" — V6 — crimps on 45°
2. "Tech overhang" — V4 — crimps with high feet
...
Rank them by best fit to the request.
```

### Option B: Instruction-Tuned Embedding Models
Use models specifically trained for retrieval and instruction-following:
- `bge-large-en` or `bge-m3`
- OpenAI's `text-embedding-3-large`

These models better understand queries like:
- "Give me a crimpy V4 with compression moves"
- "Find a technical slab problem with small footholds"

Benefits:
- Better understanding of climbing-specific terminology
- More accurate ranking based on problem characteristics
- Natural language understanding of user intent

### AI-Generated Problem Summaries
For each search result, the AI can provide a brief explanation of why the problem matches the user's query. For example:

User query: "Find a crimpy V4 with compression moves"

AI response:
```
1. "Crimpy Compression" (V4)
   - Matches your request because: This problem features sustained compression moves between small crimps on a 30° wall, requiring both finger strength and body tension. The sequence flows naturally between compression positions, making it a great example of the style you're looking for.
```

These summaries help users:
- Understand why a problem was recommended
- Quickly assess if it matches their training goals
- Learn about different problem characteristics
- Make more informed decisions about which problems to try
