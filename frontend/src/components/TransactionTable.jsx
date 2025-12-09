import '../styles/TransactionTable.css';

export function TransactionTable({ transactions, loading }) {
  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (transactions.length === 0) {
    return <div className="no-results">No transactions found</div>;
  }

  return (
    <div className="table-container">
      <table className="transaction-table">
        <thead>
          <tr>
            <th>Transaction ID</th>
            <th>Date</th>
            <th>Customer ID</th>
            <th>Customer Name</th>
            <th>Phone Number</th>
            <th>Gender</th>
            <th>Age</th>
            <th>Customer Type</th>
            <th>Product Name</th>
            <th>Brand</th>
            <th>Product Category</th>
            <th>Tags</th>
            <th>Quantity</th>
            <th>Total Amount</th>
            <th>Customer Region</th>
            <th>Product ID</th>
            <th> Employee Name</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.transaction_id}>
              <td>{transaction.transaction_id}</td>
              <td>{new Date(transaction.date).toLocaleDateString()}</td>
              <td>{transaction.customer_id}</td>
              <td>{transaction.customer_name}</td>
              <td>{transaction.phone_number}</td>
              <td>{transaction.gender}</td>
              <td>{transaction.age}</td>
              <td>{transaction.customer_type}</td>
              <td>{transaction.product_name}</td>
              <td>{transaction.brand}</td>
              <td>{transaction.product_category}</td>
              <td>{transaction.tags}</td>
              <td>{transaction.quantity}</td>
              <td>₹{transaction.total_amount.toFixed(2)}</td>
              <td>{transaction.customer_region}</td>
              <td>{transaction.product_id}</td>
              <td>{transaction.employee_name}</td>
              
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}