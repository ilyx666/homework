document.getElementById('transaction-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const account_id = document.getElementById('account_id').value;
    const amount = document.getElementById('amount').value;
    const currency = document.getElementById('currency').value;
    const transaction_type = document.getElementById('transaction_type').value;

    const transactionData = {
        account_id: parseInt(account_id),
        amount: parseFloat(amount),
        currency: currency,
        transaction_type: transaction_type
    };

    try {
        const response = await fetch('http://localhost:8000/transaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(transactionData)
        });

        const result = await response.json();
        document.getElementById('response').innerText = result.message || result.error;
    } catch (error) {
        document.getElementById('response').innerText = "ошибка: " + error.message;
    }
});
