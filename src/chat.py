from search import search_prompt


def main():
    while True:
        query = input("User: ")
        if query == "exit":
            break

        chain = search_prompt(query)

        if not chain:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return
        
        print("-"*50)
        print(f"Assistant: {chain}")
        print("-"*50)




if __name__ == "__main__":
    main()