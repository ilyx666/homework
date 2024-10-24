from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Account, Transaction
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "postgresql://postgres:123@localhost/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_account_by_id(db, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()


def update_account_balance(db, account, amount, transaction_type):
    if transaction_type == 'debit':
        if account.balance >= amount:
            account.balance -= amount
        else:
            raise ValueError("Insufficient funds")
    elif transaction_type == 'credit':
        account.balance += amount
    db.commit()


def create_transaction(db, account_id, amount, currency, transaction_type):
    new_transaction = Transaction(
        account_id=account_id,
        amount=amount,
        currency=currency,
        transaction_type=transaction_type
    )
    db.add(new_transaction)
    db.commit()
    return new_transaction
