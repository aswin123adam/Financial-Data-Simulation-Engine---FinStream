from datetime import date, datetime
from enum import Enum
from uuid import uuid4
import random
from faker import Faker
from pydantic import BaseModel, Field

class CustomerSegment(str, Enum):
    MASS = "Mass"
    MASS_AFFLUENT = "Mass Affluent"
    AFFLUENT = "Affluent"
    HIGH_NET_WORTH = "High Net Worth"

class CreditTier(str, Enum):
    POOR = "Poor"
    FAIR = "Fair"
    GOOD = "Good"
    VERY_GOOD = "Very Good"
    EXCELLENT = "Excellent"

class Customer(BaseModel):
    customer_id: str = Field(default_factory=lambda: str(uuid4()))
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: date
    city: str
    state: str
    country: str = "USA"  # Default value
    annual_income: float = Field(ge=0)  
    credit_score: int = Field(ge=300, le=850) 
    credit_tier: CreditTier
    customer_segment: CustomerSegment
    customer_since: date
    is_active: bool = True  # Default value
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CustomerGenerator:
    SEGMENT_WEIGHTS = {
        CustomerSegment.MASS: 60,
        CustomerSegment.MASS_AFFLUENT: 25,
        CustomerSegment.AFFLUENT: 12,
        CustomerSegment.HIGH_NET_WORTH: 3
    }

    INCOME_RANGES = {
        CustomerSegment.MASS: (20000, 50000),
        CustomerSegment.MASS_AFFLUENT: (50000, 100000),
        CustomerSegment.AFFLUENT: (100000, 250000),
        CustomerSegment.HIGH_NET_WORTH: (250000, 1000000)
    }

    CREDIT_SCORE_RANGES = {
        CustomerSegment.MASS: (550, 720),
        CustomerSegment.MASS_AFFLUENT: (620, 780),
        CustomerSegment.AFFLUENT: (780, 820),
        CustomerSegment.HIGH_NET_WORTH: (820, 850)
    }

    def __init__(self):
        self.fake = Faker()

    def generate_credit_tier(self, credit_score: int) -> CreditTier:
        if credit_score < 580:
            return CreditTier.POOR
        elif credit_score < 670:
            return CreditTier.FAIR
        elif credit_score < 740:
            return CreditTier.GOOD
        elif credit_score < 800:
            return CreditTier.VERY_GOOD
        else:
            return CreditTier.EXCELLENT
    
    def generate_customer(self) -> Customer:
            segment = random.choices(
            population=list(self.SEGMENT_WEIGHTS.keys()),
            weights=list(self.SEGMENT_WEIGHTS.values()),
            k=1,
            )[0]

            min_income, max_income = self.INCOME_RANGES[segment]
            income = round(random.uniform(min_income, max_income), 2)

            credit = self.CREDIT_SCORE_RANGES[segment]
            credit_score = random.randint(credit[0], credit[1])

            #Generating FAke Customer Information : 
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            email = self.fake.email()
            phone = self.fake.phone_number()
            date_of_birth = self.fake.date_of_birth(minimum_age=18, maximum_age=80)
            city = self.fake.city()
            state = self.fake.state_abbr()
            customer_since = self.fake.date_between(start_date='-10y', end_date='today')
            country = "USA"  # Default value

            # TESTING print(f"Generated Customer:\nFull Name: {first_name} {last_name},\nemail: {email} ,\nphone: {phone},\nDOB: {date_of_birth},\ncity: {city},\nstate: {state},\ncountry: {country},\ncustomer_since: {customer_since},\nGenerated Customer: {segment.value} ,\nincome: {income:,.2f},\ncredit_score: {credit_score}")

            return Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                date_of_birth=date_of_birth,
                city=city,
                state=state,
                country=country,
                annual_income=income,
                credit_score=credit_score,
                credit_tier=self.generate_credit_tier(credit_score),
                customer_segment=segment,
                customer_since=customer_since
            )
    def generate_email(self, first_name: str, last_name: str) -> str:
        domain_list = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com", "aol.com", "protonmail.com", "zoho.com", "mail.com", "gmx.com", "icloud.com", "yandex.com", "fastmail.com", "tutanota.com", "mail.ru", "hushmail.com", "airmail.net", "lycos.com", "netcourrier.com", "zimbra.com", "rediffmail.com", "mailinator.com", "freemail.de", "freemail.ru", "email.com", "email.org", "email.ru", "freeneted.de", "bigpond.com", "verizon.net", "sky.com"]
        domain = random.choice(domain_list)
        first = first_name.lower().replace(" ", "")
        last = last_name.lower().replace(" ", "")

        num = random.randint(1, 999)

        patterns = [
            f"{first}.{last}",
            f"{first}{last}",
            f"{first}{last}{num}",
            f"{first}.{last}{num}",
            f"{first}_{last}{num}",
            f"{first[0]}{last}",
            f"{first[0]}.{last}{num}",
            f"{first[0]}_{last}{num}",
            f"{first}{last[0]}",
            f"{first}.{last[0]}{num}",
            f"{first}_{last[0]}{num}",
            f"{last}.{first}",
            f"{last}{first}",
            f"{last}{first}{num}",
            f"{last}.{first}{num}",
            f"{last}_{first}{num}",
            f"{last[0]}{first}",
            f"{last[0]}.{first}{num}",
            f"{last[0]}_{first}{num}",
            f"{last}{first[0]}",
            f"{last}.{first[0]}{num}",
            f"{last}_{first[0]}{num}",
        ]

        pattern = random.choice(patterns)
        return f"{pattern}@{domain}"





if __name__ == "__main__":
    # generator = CustomerGenerator()

    # print("Testing SEGMENT_WEIGHTS distribution:")

    # generator.generate_customer()
    # for _ in range(3):
    #     customer = generator.generate_customer()
    #     print(f"Generated Customer:\nFull Name: {customer.first_name} {customer.last_name},\nemail: {customer.email} ,\nphone: {customer.phone},\nDOB: {customer.date_of_birth},\ncity: {customer.city},\nstate: {customer.state},\ncountry: {customer.country},\ncustomer_since: {customer.customer_since},\nGenerated Customer: {customer.customer_segment.value} ,\nincome: {customer.annual_income:,.2f},\ncredit_score: {customer.credit_score}")
    #     print("-" * 80)
    #     print("-" * 80)

    test_name = [("Adam", "Christo"), ("Aswin", "Muthusamy"), ("Ganga", "Hariharan")]

    for first,last in test_name:
        for _ in range(3):
            email = CustomerGenerator().generate_email(first, last)
            print(f"Generated Email for {first} {last}: {email}")