from langchain_community.document_loaders import PDFPlumberLoader
file_path = "https://www.nrigroupindia.com/e-book/Introduction%20to%20Machine%20Learning%20with%20Python%20(%20PDFDrive.com%20)-min.pdf"
loader = PDFPlumberLoader(file_path)
documents = loader.load()
print(documents)
pages = "\n".join([page.page_content for page in documents])
pages