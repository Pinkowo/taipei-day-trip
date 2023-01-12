import React from 'react';
import { Link } from "react-router-dom";

import { initializeApp } from "firebase/app"
import { getFirestore, collection, getDocs, setDoc, deleteDoc, doc } from "firebase/firestore";

const firebaseApp = initializeApp({
    apiKey: process.env.apiKey,
    authDomain: process.env.authDomain,
    projectId: process.env.projectId,
    storageBucket: process.env.storageBucket,
    messagingSenderId: process.env.messagingSenderId,
    appId: process.env.appId
});
const db = getFirestore(firebaseApp);

class TodoPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = { items: [], text: '' };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
    }

    componentDidMount() {
        const username = location.pathname.split('/')[2];
        if (username != '') {
            const takeData = async () => {
                const querySnapshot = await getDocs(collection(db, username));
                querySnapshot.forEach(doc => {
                    const newItem = {
                        text: doc.data()['text'],
                        id: doc.id,
                        handleDelete: this.handleDelete
                    };
                    this.setState(state => ({
                        items: state.items.concat(newItem)
                    }));
                });
            };
            takeData()
                .catch((err) => {
                    console.log(err);
                });
        }
    }

    render() {
        return (
            <div className="container">
                <form onSubmit={this.handleSubmit}>
                    <label htmlFor="new-todo">
                        建立你的代辦事項吧
                    </label>
                    <br />
                    <div className="input">
                        <input
                            id="new-todo"
                            onChange={this.handleChange}
                            value={this.state.text}
                        />
                        <button className="input-btn">
                            新增第 {this.state.items.length + 1} 項
                        </button>
                    </div>
                </form>
                <TodoList items={this.state.items} />
                <Link to="/" className="link-btn">返回首頁</Link>
            </div>
        );
    }

    handleChange(e) {
        this.setState({ text: e.target.value });
    }

    handleSubmit(e) {
        e.preventDefault();
        if (this.state.text.length === 0) {
            return;
        }
        let todoid = Date.now().toString();
        const newItem = {
            text: this.state.text,
            id: todoid,
            handleDelete: this.handleDelete
        };
        this.setState(state => ({
            items: state.items.concat(newItem),
            text: ''
        }));
        const username = location.pathname.split('/')[2];
        if (username != '') {
            const setData = async () => {
                await setDoc(doc(db, username, todoid), {
                    text: this.state.text
                });
            }
            setData()
                .catch((err) => {
                    console.log(err);
                });
        }
    }

    handleDelete(id) {
        let newItem = this.state.items.filter(function (item) {
            return item.id != id;
        });
        this.setState(() => ({
            items: newItem
        }));
        const username = location.pathname.split('/')[2];
        if (username != '') {
            const deleteData = async () => {
                await deleteDoc(doc(db, username, id));
            }
            deleteData()
                .catch((err) => {
                    console.log(err);
                });
        }
    }
}

class TodoList extends React.Component {
    render() {
        return (
            <ul>
                {this.props.items.map(item => (
                    <li key={item.id}>
                        {item.text}
                        <button onClick={() => { item.handleDelete(item.id) }}>刪除</button>
                    </li>
                ))}
            </ul>
        );
    }
}

export default TodoPage;