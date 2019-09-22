import React from 'react';
import ReactDOM from 'react-dom';
import ReactDataGrid from 'react-data-grid';
import { Toolbar, Data } from 'react-data-grid-addons';
import { ProgressBar, Container } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as Icons from '@fortawesome/free-solid-svg-icons';
import '../css/DataGrid.css';

class DataGrid extends React.Component {
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
    let actions = [
      {
        icon: <FontAwesomeIcon icon={Icons.faTimes} />,
        callback: () => {
          this.props.onRowDelete(row.id);
        },
      },
    ];
    const cellActions = { actions };
    return column.key === 'actions' ? cellActions[column.key] : null;
  };

  onGridRowsUpdated = ({ fromRow, toRow, updated }) => {
    if (fromRow !== toRow) {
      alert('Multiple rows HTTP PUT not allowed.');
    } else {
      const rows = this.props.rows;
      let i = fromRow;
      rows[i] = { ...rows[i], ...updated };
      this.props.onRowsChange(rows, fromRow, updated);
    }
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
