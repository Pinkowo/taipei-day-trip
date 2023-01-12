import React from 'react';
import * as ReactDOMClient from 'react-dom/client';
import HomePage from './home.jsx'
import TodoPage from './todo.jsx'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

ReactDOMClient.createRoot(document.getElementById('root')).render(
    <Router>
        <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/todo" element={<TodoPage />} />
            <Route path="/todo/:username" element={<TodoPage />} />
        </Routes>
    </Router>
)