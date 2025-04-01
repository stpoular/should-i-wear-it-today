// src/components/SubmissionManagement.js
import React, { useState, useEffect } from 'react';
import { createSubmission, getSubmissionsForUser, getSubmissionsForItem } from '../api/api';

const SubmissionManagement = () => {
  const [submissions, setSubmissions] = useState([]);
  const [newSubmission, setNewSubmission] = useState({
    item_id: '',
    comment: '',
    city: '',
    country: '',
    rating: 0,
  });

  useEffect(() => {
    const fetchSubmissions = async () => {
      const token = localStorage.getItem("token");
      try {
        const data = await getSubmissionsForUser(token);
        setSubmissions(data);
      } catch (error) {
        console.error("Error fetching submissions:", error);
      }
    };
    fetchSubmissions();
  }, []);

  const handleChange = (e) => {
    setNewSubmission({ ...newSubmission, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    try {
      const createdSubmission = await createSubmission(newSubmission, token);
      setSubmissions([...submissions, createdSubmission]);
      setNewSubmission({
        item_id: '',
        comment: '',
        city: '',
        country: '',
        rating: 0,
      });
    } catch (error) {
      console.error("Error creating submission:", error);
    }
  };

  return (
    <div>
      <h2>Submission Management</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="item_id"
          placeholder="Item ID"
          value={newSubmission.item_id}
          onChange={handleChange}
        />
        <textarea
          name="comment"
          placeholder="Comment"
          value={newSubmission.comment}
          onChange={handleChange}
        />
        <input
          type="text"
          name="city"
          placeholder="City"
          value={newSubmission.city}
          onChange={handleChange}
        />
        <input
          type="text"
          name="country"
          placeholder="Country"
          value={newSubmission.country}
          onChange={handleChange}
        />
        <input
          type="number"
          name="rating"
          placeholder="Rating"
          value={newSubmission.rating}
          onChange={handleChange}
        />
        <button type="submit">Submit Comment</button>
      </form>

      <h3>All Submissions</h3>
      <ul>
        {submissions.map((submission) => (
          <li key={submission.id}>
            <p>{submission.comment}</p>
            <p>Rating: {submission.rating}</p>
            <p>{submission.city}, {submission.country}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SubmissionManagement;
