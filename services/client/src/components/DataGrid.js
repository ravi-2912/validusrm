import React from 'react';
import ReactDOM from 'react-dom';
import ReactDataGrid from 'react-data-grid';
import { ProgressBar } from 'react-bootstrap';

const ProgressBarFormatter = ({ value }) => {
    return <ProgressBar now={value} label={`${value}%`} />;
};

const defaultColumnProperties = {
    sortable: true,
    width: 120,
    resizable: true,
};

const columns = [
    {
        key: 'id',
        name: 'ID',
        sortDescendingFirst: true,
    },
    {
        key: 'name',
        name: 'Fund Name',
        editable: true,
        width: 200,
    },
    {
        key: 'complete',
        name: 'Complete',
        formatter: ProgressBarFormatter,
        width: 300,
    },
].map(c => ({ ...c, ...defaultColumnProperties }));

const data = [
    { id: 1, name: 'fund_1', complete: 20 },
    { id: 2, name: 'fund_2', complete: 40 },
    { id: 3, name: 'fund_3', complete: 60 },
];

class DataGrid extends React.Component {
    state = {
        rows: data,
    };

    onGridRowsUpdated = ({ fromRow, toRow, updated }) => {
        const rows = this.state.rows;
        for (let i = fromRow; i <= toRow; i++) {
            rows[i] = { ...rows[i], ...updated };
        }
        this.setState({ rows });
    };

    sortRows = (initialRows, sortColumn, sortDirection) => {
        const comparer = (a, b) => {
            if (sortDirection === 'ASC') {
                return a[sortColumn] > b[sortColumn] ? 1 : -1;
            } else if (sortDirection === 'DESC') {
                return a[sortColumn] < b[sortColumn] ? 1 : -1;
            }
        };
        return sortDirection === 'NONE' ? initialRows : [...initialRows].sort(comparer);
    };

    render() {
        return (
            <ReactDataGrid
                columns={columns}
                rowGetter={i => this.state.rows[i]}
                rowsCount={this.state.rows.length}
                minHeight={500}
                onGridSort={(sortColumn, sortDirection) => {
                    this.setState({ rows: this.sortRows(data, sortColumn, sortDirection) });
                }}
                onGridRowsUpdated={this.onGridRowsUpdated}
                enableCellSelect={true}
            />
        );
    }
}

export default DataGrid;
