"""
Test script for the Humanoid Robotics Book Chatbot.
This script demonstrates how to properly test the chatbot with book-related questions.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def test_health():
    """Test the health endpoint."""
    print_section("1. Testing Health Endpoint")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def check_collection():
    """Check if documents are indexed."""
    print_section("2. Checking Vector Database Collection")
    try:
        response = requests.get(f"{BASE_URL}/chat/collection-info")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def index_documents():
    """Index the book documents."""
    print_section("3. Indexing Book Documents")
    print("⏳ This will take 5-10 minutes. Please wait...")
    print("Processing 25 MDX files with ~249 chunks...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/index",
            json={"force_reindex": False},
            timeout=600  # 10 minutes timeout
        )
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except requests.exceptions.Timeout:
        print("⚠️  Request timed out, but indexing may still be in progress.")
        print("Check the server logs: tail -f chatbot/backend/server.log")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def ask_question(question, show_sources=True):
    """Ask a question to the chatbot."""
    print(f"\n📝 Question: {question}")
    print("-" * 80)
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/query",
            json={"question": question},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Answer:\n{data['answer']}\n")
            
            if show_sources and data.get('sources'):
                print("📚 Sources:")
                for i, source in enumerate(data['sources'][:3], 1):
                    print(f"\n  [{i}] {source['title']}")
                    print(f"      Relevance: {source['similarity_score']:.2f}")
                    print(f"      Content: {source['content'][:150]}...")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_selection():
    """Test querying with selected text."""
    print_section("Testing Query with Text Selection")
    
    selected_text = """
    ROS 2 (Robot Operating System 2) is a middleware framework designed for robot control.
    It provides nodes, topics, and services for communication between different components.
    """
    
    question = "Explain the main components mentioned here in simple terms"
    
    print(f"📝 Selected Text: {selected_text.strip()}")
    print(f"\n📝 Question: {question}")
    print("-" * 80)
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/query-selection",
            json={
                "question": question,
                "selected_text": selected_text
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Answer:\n{data['answer']}\n")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_book_related_tests():
    """Run a series of book-related questions."""
    print_section("4. Testing with Book-Related Questions")
    
    # Questions organized by module
    questions = [
        # Module 1: ROS 2
        "What is ROS 2 and why is it important for robotics?",
        "Explain ROS 2 nodes, topics, and services",
        "What is URDF and what is it used for?",
        
        # Module 2: Digital Twin
        "What is a digital twin in robotics?",
        "What are the differences between Gazebo and Unity for robot simulation?",
        "How do you simulate sensors like LiDAR in Gazebo?",
        
        # Module 3: NVIDIA Isaac
        "What is NVIDIA Isaac Sim and what is it used for?",
        "Explain what Isaac ROS provides for robotics",
        "What is Nav2 and how does it help with robot navigation?",
        
        # Module 4: Vision-Language-Action
        "What is Vision-Language-Action (VLA) in robotics?",
        "How can OpenAI Whisper be used for voice commands in robotics?",
        "Explain how LLMs can be used for robot planning",
        
        # General
        "What is Physical AI?",
        "What are the main modules in this robotics course?",
        "What hardware is required for this course?",
    ]
    
    print(f"📊 Running {len(questions)} test questions...\n")
    
    successful = 0
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*80}")
        print(f"Question {i}/{len(questions)}")
        print('='*80)
        
        if ask_question(question, show_sources=True):
            successful += 1
        
        # Small delay between requests
        time.sleep(1)
    
    print_section(f"Results: {successful}/{len(questions)} questions answered successfully")

def main():
    """Main test function."""
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║              🧪 HUMANOID ROBOTICS CHATBOT - TEST SUITE 🧪                    ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Check health
    if not test_health():
        print("❌ Server is not healthy. Please check if it's running.")
        return
    
    print("✅ Server is healthy!\n")
    
    # Step 2: Check collection
    check_collection()
    
    # Step 3: Ask user if they want to index
    print("\n" + "="*80)
    print("  📊 Document Indexing Required")
    print("="*80)
    print("\nBefore asking questions, documents must be indexed.")
    print("This process takes 5-10 minutes and only needs to be done once.\n")
    
    choice = input("Do you want to index documents now? (y/n): ").lower()
    
    if choice == 'y':
        if index_documents():
            print("\n✅ Documents indexed successfully!")
        else:
            print("\n⚠️  Indexing may be in progress. Check server logs.")
            print("You can continue and try asking questions anyway.")
    
    # Step 4: Run test questions
    print("\n" + "="*80)
    choice = input("\nDo you want to test with book-related questions? (y/n): ").lower()
    
    if choice == 'y':
        run_book_related_tests()
    
    # Step 5: Test with selection
    print("\n" + "="*80)
    choice = input("\nDo you want to test query with text selection? (y/n): ").lower()
    
    if choice == 'y':
        test_with_selection()
    
    # Step 6: Interactive mode
    print_section("Interactive Mode")
    print("You can now ask custom questions. Type 'quit' to exit.\n")
    
    while True:
        question = input("\n💬 Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        if question:
            ask_question(question)
    
    print("\n" + "="*80)
    print("  ✅ Testing Complete!")
    print("="*80)
    print("\n📚 For more information, visit: http://localhost:8000/docs\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
