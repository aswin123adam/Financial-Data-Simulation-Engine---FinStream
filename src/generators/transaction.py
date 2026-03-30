from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field
import random
from uuid import uuid4

class TransactionType(str, Enum):
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    PURCHASE = "Purchase"
    TRANSFER_IN = "Transfer In"
    TRANSFER_OUT = "Transfer Out"
    PAYMENT = "Payment"
    REFUND = "Refund"
    CARD_AUTHORIZATION = "Card Authorization"

class TransactionCategory(str, Enum):
    GROCERIES = "Groceries"
    UTILITIES = "Utilities"
    ENTERTAINMENT = "Entertainment"
    RESTAURANTS = "Restaurants"
    TRAVEL = "Travel"
    SHOPPING = "Shopping"
    HEALTHCARE = "Healthcare"
    GAS= "Gas"
    OTHER = "Other"

class Transaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid4()))
    customer_id: str
    transaction_type: TransactionType
    transaction_category: TransactionCategory
    amount: float = Field(ge=0)  
    merchant: str = ""
    transaction_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    description: str = ""


class TransactionGenerator:

    TYPES_WITH_CATEGORY = [
        TransactionType.PURCHASE,
        TransactionType.PAYMENT,
    ]
    
    TYPES_WITH_MERCHANT = [
        TransactionType.PURCHASE,
        TransactionType.PAYMENT,
        TransactionType.REFUND,
    ]

    MERCHANTS = {
    TransactionCategory.GROCERIES: ["Whole Foods", "Trader Joe's", "Safeway", "Albertsons", "Kroger", "Publix", "Harris Teeter", "H-E-B", "Meijer", "Hy-Vee", "Giant", "Giant Eagle", "Wegmans", "Food Lion", "Winn-Dixie", "Aldi", "Lidl", "Walmart Supercenter", "Target Grocery"],
    TransactionCategory.UTILITIES: ["PG&E", "Southern California Edison", "Con Edison", "Duke Energy", "Dominion Energy", "Xcel Energy", "National Grid", "Pacific Gas & Electric", "ComEd", "CenterPoint Energy", "Comcast", "Xfinity", "Verizon", "AT&T", "T-Mobile", "Spectrum", "Frontier"],
    TransactionCategory.ENTERTAINMENT: ["Netflix", "Spotify", "Hulu", "Disney+", "HBO Max", "Apple TV+", "YouTube Premium", "Amazon Prime Video", "ESPN+", "Apple Music", "Pandora", "Xbox Game Pass", "Xbox Live", "PlayStation Plus", "Nintendo eShop", "Ticketmaster", "Live Nation", "Fandango"],
    TransactionCategory.RESTAURANTS: ["McDonald's", "Starbucks", "Chipotle", "Subway", "Taco Bell", "KFC", "Burger King", "Wendy's", "Domino's", "Pizza Hut", "Papa John's", "Chick-fil-A", "Panera Bread", "Shake Shack", "Five Guys", "In-N-Out Burger", "Dunkin'", "Whataburger", "Sonic"],
    TransactionCategory.TRAVEL: ["Delta Airlines", "American Airlines", "United Airlines", "Southwest Airlines", "JetBlue", "Alaska Airlines", "Frontier Airlines", "Spirit Airlines", "Marriott Hotels", "Hilton Hotels", "Hyatt", "IHG", "Motel 6", "Airbnb", "Uber", "Lyft", "Enterprise", "Hertz", "Avis", "Budget"],
    TransactionCategory.SHOPPING: ["Amazon", "Walmart", "Target", "Best Buy", "Home Depot", "Lowe's", "Costco", "Sam's Club", "Macy's", "Kohl's", "JCPenney", "Gap", "Old Navy", "H&M", "Zara", "Apple Store", "Nike", "Sephora", "Ulta Beauty", "Michaels", "HomeGoods"],
    TransactionCategory.HEALTHCARE: ["CVS Pharmacy", "Walgreens", "Rite Aid", "Walmart Pharmacy", "Target Pharmacy", "Kroger Pharmacy", "Giant Pharmacy", "Mayo Clinic", "Cleveland Clinic", "Kaiser Permanente", "Johns Hopkins", "LabCorp", "Quest Diagnostics"],
    TransactionCategory.GAS: ["Shell", "ExxonMobil", "Chevron", "Mobil", "BP", "Marathon", "76", "Sunoco", "Phillips 66", "Conoco", "Valero", "Speedway", "Circle K", "Wawa", "Sheetz", "QuikTrip", "Love's Travel Stops", "Pilot Flying J"],
    TransactionCategory.OTHER: ["Miscellaneous Merchant", "PayPal", "Venmo", "Zelle", "Stripe", "Square", "Cash App", "Apple Pay", "Google Pay", "Western Union", "MoneyGram"],
    }

    AMOUNT_RANGES = {
        TransactionType.DEPOSIT: (100, 5000),
        TransactionType.WITHDRAWAL: (20, 500),
        TransactionType.PURCHASE: (5, 500),
        TransactionType.TRANSFER_IN: (50, 2000),
        TransactionType.TRANSFER_OUT: (50, 2000),
        TransactionType.PAYMENT: (50, 1000),
        TransactionType.REFUND: (5, 200),
        TransactionType.CARD_AUTHORIZATION: (0, 0)
    }

    CATEGORY_AMOUNT_RANGES = {
        TransactionCategory.GROCERIES: (20, 200),
        TransactionCategory.UTILITIES: (50, 300),
        TransactionCategory.ENTERTAINMENT: (5, 50),
        TransactionCategory.RESTAURANTS: (5, 100),
        TransactionCategory.TRAVEL: (50, 2000),
        TransactionCategory.SHOPPING: (10, 500),
        TransactionCategory.HEALTHCARE: (10, 500),
        TransactionCategory.GAS: (20, 80),
        TransactionCategory.OTHER: (5, 200)
    }
    

    def generate_transaction(self) -> Transaction:
        transaction_id = str(uuid4())
        customer_id = random.choice(self.customer_ids)
        transaction_type = random.choice(list(TransactionType))
        
        if transaction_type in self.TYPES_WITH_CATEGORY:
            category = random.choice(list(TransactionCategory))
            merchant = random.choice(self.MERCHANTS[category])
        elif transaction_type in self.TYPES_WITH_MERCHANT:
            category = TransactionCategory.OTHER
            merchant = random.choice(self.MERCHANTS[category])
        else:
            category = TransactionCategory.OTHER
            merchant = ""
        
        if transaction_type in self.TYPES_WITH_CATEGORY:
            min_amount, max_amount = self.CATEGORY_AMOUNT_RANGES[category]

        else:
            min_amount, max_amount = self.AMOUNT_RANGES[transaction_type]

        if min_amount == max_amount:
            amount = min_amount
        else:
            amount = round(random.uniform(min_amount, max_amount), 2)

        
        transaction_date = datetime.now(timezone.utc)
        description = f"{transaction_type.value} for {category.value} at {merchant}" if merchant else transaction_type.value
        return Transaction(
            transaction_id=transaction_id,
            customer_id=customer_id,
            transaction_type=transaction_type,
            transaction_category=category,
            amount=amount,
            merchant=merchant,
            transaction_date=transaction_date,
            description=description
        )


    def __init__(self, customer_ids: list[str]):
        if not customer_ids:
            raise ValueError("Customer IDs list cannot be empty.")
        self.customer_ids = customer_ids
        

if __name__ == "__main__":
    CUSTOMER_LIST = ["1lskanfa93","2lskanfa93","3lskanfa93","4lskanfa93","5lskanfa93","6lskanfa93","7lskanfa93","8lskanfa93","9lskanfa93","1skanfa93"]

    generator = TransactionGenerator(CUSTOMER_LIST)

    for i in range(3):
        transaction = generator.generate_transaction()

        print(f"Generated transaction: {transaction.transaction_id}")
        print(f"Customer ID: {transaction.customer_id}")
        print(f"Type: {transaction.transaction_type.value}")
        print(f"Category: {transaction.transaction_category.value}")
        print(f"Amount: ${transaction.amount:,.2f}")
        print(f"Merchant: {transaction.merchant}")
        print(f"Date: {transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Description: {transaction.description}")

        print("-" * 80)
        print("-" * 80)