import React from 'react';
import ReactDOM from 'react-dom';
import ReactDataGrid from 'react-data-grid';
import { Toolbar, Data } from 'react-data-grid-addons';
import { ProgressBar, Container } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as Icons from '@fortawesome/free-solid-svg-icons';

import '../css/DataGrid.css';

const ProgressBarFormatter = ({ value }) => {
  return <ProgressBar now={value} label={`${value}%`} />;
};

const defaultColumnProperties = {
  resizable: true,
  filterable: true,
};

const columns = [
  {
    key: 'id',
    name: 'ID',
    sortDescendingFirst: true,
    sortable: true,
    width: 120,
  },
  {
    key: 'name',
    name: 'Fund Name',
    editable: true,
    sortable: true,
    width: 250,
  },
  {
    key: 'complete',
    name: 'Complete',
    formatter: ProgressBarFormatter,
    sortable: true,
  },
  {
    key: 'actions',
    name: 'Actions',
    width: 120,
  },
].map(c => ({ ...c, ...defaultColumnProperties }));

const data = [
  { id: 1, name: 'fund_1', complete: 20 },
  { id: 2, name: 'fund_2', complete: 40 },
  { id: 3, name: 'fund_3', complete: 60 },
];

class DataGrid extends React.Component {
  state = {
    rows: [data],
    filters: {},
  };

  actions = [
    {
      icon: <FontAwesomeIcon icon={Icons.faTimes} />,
      callback: () => {
        alert('Deleting');
      },
    },
  ];

  handleFilterChange = filter => {
    const newFilters = { ...this.state.filters };
    if (filter.filterTerm) {
      newFilters[filter.column.key] = filter;
    } else {
      delete newFilters[filter.column.key];
    }
    this.setState({ filters: newFilters });
  };

  getRows = (rows, filters) => {
    return Data.Selectors.getRows({ rows, filters });
  };

  getCellActions = (column, row) => {
    const cellActions = {
      actions: this.actions,
    };
    return cellActions[column.key];
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
    const filteredRows = this.getRows(this.state.rows, this.state.filters);
    return (
      <ReactDataGrid
        className="DataGrid"
        columns={columns}
        rowGetter={i => filteredRows[i]}
        rowsCount={filteredRows.length}
        minHeight={500}
        minColumnWidth={120}
        onGridSort={(sortColumn, sortDirection) => {
          this.setState({ rows: this.sortRows(data, sortColumn, sortDirection) });
        }}
        onGridRowsUpdated={this.onGridRowsUpdated}
        enableCellSelect={true}
        getCellActions={this.getCellActions}
        toolbar={<Toolbar enableFilter={true} />}
        onAddFilter={filter => this.handleFilterChange(filter)}
        onClearFilters={() => this.setState({ filters: {} })}
      />
    );
  }
}

export default DataGrid;
