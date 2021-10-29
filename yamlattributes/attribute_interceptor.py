class AttributeInterceptor(type):
    def __getattr__(cls, key):
        retrieval_mode = super().__getattribute__('__retrieval_mode')

        if retrieval_mode == 'safe':
            return None

        return super().__getattribute__(key)
