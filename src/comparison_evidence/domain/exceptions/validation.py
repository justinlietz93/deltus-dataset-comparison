class ContractValidationError(ValueError):
    def __init__(self, messages: list[str] | tuple[str, ...]):
        self.messages = tuple(messages)
        super().__init__("; ".join(self.messages))
