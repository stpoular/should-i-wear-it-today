// src/components/ItemManagement.js
import React, { useState, useEffect } from 'react';
import { createItem, getItems } from '../api/api';

const ItemManagement = () => {
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState({ name: '', color: '' });

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const data = await getItems();
        setItems(data);
      } catch (error) {
        console.error("Error fetching items:", error);
      }
    };
    fetchItems();
  }, []);

  const handleChange = (e) => {
    setNewItem({ ...newItem, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    try {
      const createdItem = await createItem(newItem, token);
      setItems([...items, createdItem]);
      setNewItem({ name: '', color: '' });
    } catch (error) {
      console.error("Error creating item:", error);
    }
  };

  return (
    <div>
      <h2>Item Management</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Item Name"
          value={newItem.name}
          onChange={handleChange}
        />
        <input
          type="text"
          name="color"
          placeholder="Item Color"
          value={newItem.color}
          onChange={handleChange}
        />
        <button type="submit">Create Item</button>
      </form>

      <h3>All Items</h3>
      <ul>
        {items.map((item) => (
          <li key={item.id}>{item.name} - {item.color}</li>
        ))}
      </ul>
    </div>
  );
};

export default ItemManagement;
