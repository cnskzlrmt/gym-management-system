from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 1. Spor salonu ile ilgili örnek dokümanlar (Document nesnelerine dönüştürülmüş)
documents = [
    Document(page_content="Spor salonumuz, profesyonel antrenörler eşliğinde fitness, kardiyo ve ağırlık antrenmanı hizmeti sunmaktadır."),
    Document(page_content="Üyelik paketlerimiz: Aylık, yıllık, öğrenci ve aile üyelikleri mevcuttur."),
    Document(page_content="Spor salonumuzda grup dersleri, yoga ve pilates seansları düzenlenmektedir."),
    Document(page_content="Kişisel antrenman ve diyet planı hizmetlerimiz ile bireysel ihtiyaçlara yönelik destek sunmaktayız."),
]

# 2. Dokümanları parçalar halinde bölüyoruz
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# 3. Embedding modelini kullanarak vektör veritabanı oluşturuyoruz
embeddings = OpenAIEmbeddings()  # API anahtarınızı uygun şekilde yapılandırmayı unutmayın
vector_store = FAISS.from_texts([doc.page_content for doc in docs], embeddings)

# 4. RetrievalQA zinciri oluşturulması
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})
qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)

# Örnek sorgu: Grup dersleri hakkında bilgi alma
query = "Spor salonumuzdaki grup dersleri hakkında bilgi verir misin?"
result = qa_chain.run(query)
print(result)
