from search import search_prompt


def main():
    while True:
        query = input("USER: ")
        if query == "exit":
            break

        chain = search_prompt(query)

        if not chain:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return
        
        print("-"*50)
        print(f"ASSISTANT: {chain}")
        print("-"*50)




if __name__ == "__main__":
    main()