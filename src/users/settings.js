import React from 'react';
import ReactDom from 'react-dom';
import getCookie from '../utils/get_cookie';

class UserSettings extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: context.user,
            tags: context.tags,
            updatedUser: Object.assign({}, context.user),
            tag: '',
        };

        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.handleFirstNameEdit = this.handleFirstNameEdit.bind(this);
        this.handleLastNameEdit = this.handleLastNameEdit.bind(this);
        this.handleTagFormSubmit = this.handleTagFormSubmit.bind(this);
        this.handleTagInput = this.handleTagInput.bind(this);
        this.handleDeleteTags = this.handleDeleteTags.bind(this);
    }

    handleFormSubmit(e) {
        e.preventDefault();

        fetch('/api/user/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(this.state.updatedUser)
        }).then(response => {
            if(response.status === 200) {
                response.json().then(json => {
                    this.setState({
                        user: json,
                    });
                });
            }
        }).catch(err => {
            alert('Error updating');
        });
    }

    handleFirstNameEdit(e) {
        let user = this.state.updatedUser;  
        
        user.first_name = e.target.value;

        this.setState({
            updatedUser: user
        });
    }

    handleLastNameEdit(e) {
        let user = this.state.updatedUser;

        user.last_name = e.target.value;

        this.setState({
            updatedUser: user
        });
    }

    handleTagFormSubmit(e) {
        e.preventDefault();

        if(this.state.tag.length < 3) {
            alert('Tag must be minimum of 3 chars length');
            return;
        }

        fetch('/api/user/tags/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                title: this.state.tag
            })
        }).then(response => {
            if(response.status === 200) {
                response.json().then(json => {
                    let tags = this.state.tags;

                    tags.push(json);

                    this.setState({
                        tags: tags,
                        tag: ''
                    });
                });
            } else {
                alert('Tag already added');
            }
        }).catch(err => {
            alert('Error adding tag');
        });
    }

    handleTagInput(e) {
        this.setState({
            tag: e.target.value
        });
    }

    handleDeleteTags(e, uuid) {
        fetch('/api/user/tags/', {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                uuid: uuid
            })
        }).then(response => {
            if(response.status === 200) {
                let tags = this.state.tags;

                tags = tags.filter((value) => {
                    return value.uuid !== uuid;
                });

                this.setState({
                    tags: tags
                });
            } else {
                alert('Error removing tag');
            }
        }).catch(err => {
            alert('Error removing tag');
        });
    }
    
    render() {
        return (
            <div className="container">
                <div className="row">
                    <div className="col s12 margin-top">
                        <center>
                            <h3>
                                <i className="material-icons large circle green">person</i>
                                <br/>{this.state.user.first_name} {this.state.user.last_name}
                            </h3>

                            <p>
                                @{this.state.user.username} | {this.state.user.email}
                            </p>
                        </center>
                    </div>
                </div>

                <div className="row">
                    <div className="col s12">
                        <form ref="form" onSubmit={this.handleFormSubmit}>
                            <div className="row">
                                <div className="col s6 input-field">
                                    <input type="text" className="validate" id="first_name" value={this.state.updatedUser.first_name} onChange={this.handleFirstNameEdit}></input>
                                    <label htmlFor="first_name">First name</label>
                                </div>
                                <div className="col s6 input-field">
                                    <input type="text" className="validate" id="last_name" value={this.state.updatedUser.last_name} onChange={this.handleLastNameEdit}></input>
                                    <label htmlFor="last_name">Last name</label>
                                </div>
                            </div>

                            <div className="row">

                            </div>

                            <center>
                                <button className="btn" type="submit">Save</button>
                            </center>
                        </form>
                    </div>
                </div>

                <div className="row">
                    <div className="col m2 hide-on-small-only"></div>
                    <div className="col m8 s12">
                        {
                            this.state.tags.map((tag, index) => {
                                return (
                                    <div className="chip" key={index}>
                                        <span>{tag.title}</span>
                                        <i className="material-icons click" onClick={(e) => {this.handleDeleteTags(e, tag.uuid)}}>close</i>
                                    </div>
                                );
                            })
                        }
                    </div>
                </div>

                <div className="row">
                    <div className="col m2 hide-on-small-only"></div>
                    <div className="col m8 s12">
                        <form ref="form" onSubmit={this.handleTagFormSubmit}>
                            <div className="row input-field">
                                <input type="text" className="validate" id="tag" value={this.state.tag} onChange={this.handleTagInput}></input>
                                <label htmlFor="tag">+Tag</label>
                            </div>
                            <center>
                                <button className="btn" type="submit">Submit</button>
                            </center>
                        </form>
                    </div>
                </div>
            </div>
        );
    }
}

ReactDom.render(
    <UserSettings />,
    document.getElementById('root')    
);
