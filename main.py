from src.virtual_machine import VirtualMachine

def main():
    vm = VirtualMachine("program.code")
    vm.run()

if __name__ == "__main__":
    main()