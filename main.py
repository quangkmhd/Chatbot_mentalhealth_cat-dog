import os
import fitz  # PyMuPDF
import pickle
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.docstore.document import Document
from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message  # For chat UI
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import nltk
from prompt_template import PET_MENTAL_HEALTH_TEMPLATE
nltk.download('punkt')      # Tokenizer cơ bản
nltk.download('punkt_tab')
load_dotenv()

# HuggingFace API token
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Directories for PDF and vector store
DATA_DIR = "data"
FAISS_PATH = os.path.join(DATA_DIR, "pet_mental_health_vector_store.pkl")
HISTORY_PATH = os.path.join(DATA_DIR, "chat_history.pkl")  # Define HISTORY_PATH globally

os.makedirs(DATA_DIR, exist_ok=True)

# Function to save uploaded PDF file
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(DATA_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Extract text from PDF with error handling
def extract_text_from_pdf(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            text = "\n".join([page.get_text("text").strip() for page in doc])
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

# Create vector embeddings and save to FAISS
def create_vector_store(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    if not pdf_text:
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_text(pdf_text)

    documents = [Document(page_content=t) for t in texts]
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if os.path.exists(FAISS_PATH):
        try:
            with open(FAISS_PATH, "rb") as f:
                vector_store = pickle.load(f)
            vector_store.add_documents(documents)
        except Exception as e:
            print(f"Error loading vector store: {e}. Creating new one.")
            vector_store = FAISS.from_documents(documents, embeddings)
    else:
        vector_store = FAISS.from_documents(documents, embeddings)
    
    with open(FAISS_PATH, "wb") as f:
        pickle.dump(vector_store, f)

    return vector_store

# Load LLM from HuggingFace
def load_llm():
    return HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        max_length=2048,
        temperature=0.1,
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    )

# Query documents from FAISS with limit
def retrieve_docs(vector_store, query, top_k=4):
    retriever = vector_store.as_retriever(search_kwargs={"k": top_k})
    return retriever.get_relevant_documents(query)

# Pet mental health chatbot function
def pet_mental_health_chat(pet_condition, vector_store):
    if vector_store is None:
        return "Please upload a pet mental health PDF document first."
    
    llm = load_llm()
    docs = retrieve_docs(vector_store, pet_condition)

    if not docs:
        return "No relevant information found about this pet condition."

    context = "\n\n".join([doc.page_content for doc in docs])

    # Sử dụng template từ file riêng
    prompt = ChatPromptTemplate.from_template(PET_MENTAL_HEALTH_TEMPLATE)
    chain = prompt | llm

    return chain.invoke({"pet_condition": pet_condition, "context": context})

# Save chat history
def save_chat_history(history):
    with open(HISTORY_PATH, "wb") as f:  # Use globally defined HISTORY_PATH
        pickle.dump(history, f)

# Load chat history
def load_chat_history():
    if os.path.exists(HISTORY_PATH):  # Use globally defined HISTORY_PATH
        with open(HISTORY_PATH, "rb") as f:
            return pickle.load(f)
    return []

# Streamlit interface
# Save chat history
def save_chat_history(history):
    with open(HISTORY_PATH, "wb") as f:
        pickle.dump(history, f)

# Load chat history
def load_chat_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "rb") as f:
            return pickle.load(f)
    return []

# Tập câu trả lời chuẩn (ground truth) - mở rộng theo nhu cầu
# Tập câu trả lời chuẩn (ground truth)
# Tập câu trả lời chuẩn (ground truth)
REFERENCE_RESPONSES = {
    "Hiding a lot": [
        """
Based on the symptoms provided, the most likely mental health conditions for your cat are:

**Depression – 70% likely**  
**Anxiety – 60% likely**  
**Hiding behavior due to pain or discomfort – 50% likely**

**Detailed Description of Each Condition**  
*Depression:* This condition can occur in cats due to various reasons such as loss of a companion, change in environment, or chronic illness. Symptoms include hiding, loss of appetite, and lethargy.  
*Anxiety:* This is often triggered by changes in the cat's environment or routine. Symptoms include hiding, excessive meowing, and changes in appetite.  
*Hiding behavior due to pain or discomfort:* Cats often hide when they are not feeling well. This could be due to dental disease, arthritis, or other physical discomforts.

**Recommended Treatment Approaches**  
*Depression:* Try to maintain a consistent routine for your cat. Spend more quality time with them, provide interactive toys, and consider playing calming music. If the condition persists, consult with a veterinarian about potential medication.  
*Anxiety:* Identify and eliminate (if possible) the source of anxiety. Provide hiding places, use pheromone diffusers, and consider desensitization and counterconditioning techniques. If the anxiety is severe, consult with a veterinarian about potential medication.  
*Hiding behavior due to pain or discomfort:* Consult with a veterinarian for a thorough check-up. Treatment will depend on the underlying cause. It could range from medication for dental disease to pain relief for arthritis.

**When to Consult a Veterinarian or Specialist**  
If your cat's condition does not improve within a week, or if the symptoms worsen, consult with a veterinarian immediately. If your cat is vomiting or has difficulty swallowing, these are red flags that require urgent professional evaluation.

**If Data is Incomplete → Ask Follow-Up Questions**  
To better distinguish between the top suspected conditions, it would be helpful to know:  
- Has there been a recent change in your cat's environment or routine?  
- Have you noticed any changes in your cat's urinary or defecation habits?
        """,
        # Biến thể ngắn hơn để tăng linh hoạt cho BLEU Score
        "Your cat might be depressed (70%) or anxious (60%) due to hiding a lot. Spend time with them or see a vet if it persists."
    ],
    "Not eating": ["Loss of appetite might indicate stress, illness, or dental issues. Monitor for 24 hours and see a vet if it continues."],
    "Excessive barking/meowing": ["This may be due to anxiety, boredom, or attention-seeking. Try enrichment activities and consult a vet if excessive."],
    "Lethargic": ["Lethargy can signal depression or a medical issue. Check for other symptoms and visit a vet if it lasts more than a day."]
}

# Hàm tính BLEU Score
def calculate_bleu(reference_texts, candidate_text):
    references = [nltk.word_tokenize(ref.lower()) for ref in reference_texts]
    candidate = nltk.word_tokenize(candidate_text.lower())
    smoothie = SmoothingFunction().method1
    score = sentence_bleu(references, candidate, weights=(0.5, 0.5, 0, 0), smoothing_function=smoothie)  # Chỉ dùng 1-gram và 2-gram
    return score

# Streamlit interface
def main():
    st.set_page_config(page_title="Pet Mental Health Assistant", layout="wide", initial_sidebar_state="expanded")

    # Sidebar for Pet Profile and FAQ
    with st.sidebar:
        st.title("🐾 Pet Profile")
        if 'pet_profiles' not in st.session_state:
            st.session_state.pet_profiles = {}

        profile_name = st.text_input("Pet Name")
        pet_type = st.selectbox("Pet Type", ["Dog", "Cat"])
        pet_age = st.number_input("Age (years)", min_value=0, max_value=30, step=1)
        pet_breed = st.text_input("Breed")
        pet_weight = st.number_input("Weight (kg)", min_value=0.1, step=0.1)
        pet_gender = st.radio("Gender", ["Male", "Female", "Unknown"])
        pet_vaccinated = st.checkbox("Vaccinated?")

        if st.button("Save Pet Profile") and profile_name:
            st.session_state.pet_profiles[profile_name] = {
                "type": pet_type, "age": pet_age, "breed": pet_breed,
                "weight": pet_weight, "gender": pet_gender, "vaccinated": pet_vaccinated
            }
            st.success(f"✅ Saved profile for {profile_name}!")

        selected_pet = st.selectbox("Select Pet", ["None"] + list(st.session_state.pet_profiles.keys()))

        st.subheader("📚 FAQ")
        with st.expander("Common Questions"):
            st.markdown("""
            - **How often should I vaccinate my pet?** Yearly boosters are recommended after initial shots! 🩺  
            - **What’s a good diet for my pet?** Balanced food with protein, fats, and carbs—ask your vet! 🍗  
            - **When to deworm?** Every 3-6 months, depending on lifestyle! 🐛
            """)

    # Main content
    st.title("🐾 Pet Mental Health Assistant")
    st.markdown("Hi there! I’m your friendly vet assistant. Upload a PDF or chat with me about your pet’s mental health! 😊")

    # Initialize session state
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
        if os.path.exists(FAISS_PATH):
            try:
                with open(FAISS_PATH, "rb") as f:
                    st.session_state.vector_store = pickle.load(f)
                st.success("✅ Loaded pet mental health database!")
            except:
                st.warning("No existing database found.")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = load_chat_history()

    # File uploader
    upload_file = st.file_uploader("📂 Upload a Pet Mental Health PDF", type="pdf")
    if upload_file:
        with st.spinner("🔄 Processing PDF..."):
            file_path = save_uploaded_file(upload_file)
            st.session_state.vector_store = create_vector_store(file_path)
        st.success("✅ PDF processed successfully!")

    # Chat Interface
    st.subheader("💬 Chat with Your Vet Assistant")
    col1, col2 = st.columns([3, 1])

    with col1:
        for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
            message(user_msg, is_user=True, key=f"user_{i}")
            message(bot_msg, key=f"bot_{i}")

        pet_condition = st.text_area("Tell me about your pet’s symptoms:", placeholder="E.g., My cat is hiding a lot...")
        if selected_pet != "None":
            pet_info = st.session_state.pet_profiles[selected_pet]
            pet_context = f"{pet_info['type']} ({pet_info['breed']}), {pet_info['age']} years, {pet_info['weight']}kg, {pet_info['gender']}, Vaccinated: {pet_info['vaccinated']}"
            full_query = f"{pet_context} - Symptoms: {pet_condition}"
        else:
            full_query = pet_condition

    

    if st.button("🐾 Get Analysis") and pet_condition:
        if st.session_state.vector_store:
            with st.spinner("🔍 Analyzing..."):
                response = pet_mental_health_chat(full_query, st.session_state.vector_store)
                st.write("**Chatbot Response:**", response)  # In câu trả lời để kiểm tra
                bleu_score = None
                for key in REFERENCE_RESPONSES:
                    if key.lower() in pet_condition.lower():
                        bleu_score = calculate_bleu(REFERENCE_RESPONSES[key], response)
                        break
                if bleu_score is not None:
                    st.session_state.last_bleu = bleu_score
                else:
                    st.session_state.last_bleu = "N/A (No reference available)"
                st.session_state.chat_history.append((full_query, response))
                save_chat_history(st.session_state.chat_history)
                message(full_query, is_user=True, key="user_symptoms")
                message(response, key="bot_symptoms")
                st.write(f"**BLEU Score:** {st.session_state.last_bleu if st.session_state.last_bleu == 'N/A' else f'{st.session_state.last_bleu:.2f}'}")
    # Symptom Checklist
    st.subheader("✅ Symptom Checklist")
    symptoms = ["Fever", "Vomiting", "Diarrhea", "Loss of Appetite", "Coughing", "Itching"]
    selected_symptoms = st.multiselect("Check any symptoms you’ve noticed:", symptoms)
    if selected_symptoms:
        st.write(f"Selected symptoms: {', '.join(selected_symptoms)}")
        if st.button("Analyze Symptoms"):
            full_query += f" - Symptoms: {', '.join(selected_symptoms)}"
            response = pet_mental_health_chat(full_query, st.session_state.vector_store)
            # Tính BLEU Score
            bleu_score = None
            for key in REFERENCE_RESPONSES:
                if key.lower() in full_query.lower():
                    bleu_score = calculate_bleu(REFERENCE_RESPONSES[key], response)
                    break
            if bleu_score is not None:
                st.session_state.last_bleu = bleu_score
            else:
                st.session_state.last_bleu = "N/A (No reference available)"

            st.session_state.chat_history.append((full_query, response))
            save_chat_history(st.session_state.chat_history)
            message(full_query, is_user=True, key="user_symptoms")
            message(response, key="bot_symptoms")
            st.write(f"**BLEU Score:** {st.session_state.last_bleu if st.session_state.last_bleu == 'N/A' else f'{st.session_state.last_bleu:.2f}'}")


if __name__ == "__main__":
    main()