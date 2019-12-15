import React from 'react';
import ReactDom from 'react-dom';
import GroupCard from '../components/groups/group_card';

class UserGroups extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            groups: context.groups,
            ownedGroups: context.owned_groups
        };
    }

    render() {
        return (
            <div className="container">
                <div className="row">
                    <div className="col m2 s12 margin-top">
                        <center>
                        <a className="btn" href="/groups/create/">New group</a>
                        </center>
                    </div>
                    <div className="col m8 s12 margin-top">
                        <div className="row">
                            <ul className="tabs">
                                <li className="tab col s6">
                                    <a href="#all">All groups</a>
                                </li>
                                <li className="tab col s6">
                                    <a href="#owned">Owned groups</a>
                                </li>
                            </ul>
                        </div>
                        <div className="row">
                            <div id="all">
                                {this.state.groups.map((group, index) => {
                                    return <GroupCard group={group} key={index} />
                                })}
                            </div>
                            <div id="owned">
                                {this.state.ownedGroups.map((group, index) => {
                                    return <GroupCard group={group} key={index} />
                                })}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

ReactDom.render(
    <UserGroups />,
    document.getElementById('root')
);
