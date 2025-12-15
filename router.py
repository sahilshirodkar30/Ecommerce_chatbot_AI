from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.index import LocalIndex

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name='faq',
    utterances=[
        "What is the return policy of the products?",
        "What is your policy on defective products?",
        "How do I return a damaged product?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
    ]
)


sql = Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
    ]
)

smalltalk = Route(
    name='smalltalk',
    utterances=[
    "How are you?",
     "What is your name?",
    "Are you a robot?",
     "What are you?",
    "What do you do?",
    ]
)
index = LocalIndex(
    index_path=".semantic_router"
)


router = SemanticRouter(encoder=encoder, routes=[faq, sql,smalltalk], index=index,auto_sync="local")




if __name__ == "__main__":
    r1 = router("What is your policy on defective product?")
    print(r1.name if r1 else "No route matched")

    r2 = router("Pink Puma shoes in price range 5000 to 1000")
    print(r2.name if r2 else "No route matched")
    r3 = router("How are you?")
    print(r3.name if r3 else "No route matched")
