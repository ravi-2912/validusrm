import React from 'react';
import ReactDOM from 'react-dom';
import ReactDataGrid from 'react-data-grid';
import { Toolbar, Data } from 'react-data-grid-addons';
import { ProgressBar, Container } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as Icons from '@fortawesome/free-solid-svg-icons';
import '../css/DataGrid.css';

class DataGrid extends React.Component {
  actions = [
    {
      icon: <FontAwesomeIcon icon={Icons.faTimes} />,
      callback: () => {
        alert('Deleting');
      },
    },
  ];

  handleFilterChange = filter => {
    const newFilters = { ...this.props.filters };
    if (filter.filterTerm) {
      newFilters[filter.column.key] = filter;
    } else {
      delete newFilters[filter.column.key];
    }
    this.props.onFiltersChange(newFilters);
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
    const rows = this.props.rows;
    for (let i = fromRow; i <= toRow; i++) {
      rows[i] = { ...rows[i], ...updated };
    }
    this.props.onRowsChange(rows);
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
    const filteredRows = this.getRows(this.props.rows, this.props.filters);
    return (
      <ReactDataGrid
        className="DataGrid"
        columns={this.props.columns}
        rowGetter={i => filteredRows[i]}
        rowsCount={filteredRows.length}
        minColumnWidth={120}
        onGridSort={(sortColumn, sortDirection) => {
          this.props.onRowsChange(this.sortRows(this.props.rows, sortColumn, sortDirection));
        }}
        onGridRowsUpdated={this.onGridRowsUpdated}
        enableCellSelect={true}
        getCellActions={this.getCellActions}
        toolbar={
          <Toolbar
            enableFilter={true}
            onAddRow={({ newRowIndex }) => this.props.onAddRow(newRowIndex)}
          />
        }
        onAddFilter={filter => this.handleFilterChange(filter)}
        onClearFilters={() => this.setState({ filters: {} })}
      />
    );
  }
}

export default DataGrid;
