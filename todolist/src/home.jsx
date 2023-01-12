import React, { useState } from 'react';
import { Link } from "react-router-dom";

const HomePage = () => {
    const [username, setName] = useState("");
    return (
        <div className="container">
            <h1>歡迎使用 Todo List</h1>
            <input
                type="text"
                id="user-name"
                className='name-input'
                placeholder="請輸入您的大名"
                onChange={(e) => { setName(e.target.value) }}
            />
            <Link to={`/todo/${username}`} className="link-btn">點此開始</Link>
        </div>
    )
}

export default HomePage;
