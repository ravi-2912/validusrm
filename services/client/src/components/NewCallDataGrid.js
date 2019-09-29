import React from 'react';
import PropTypes from 'prop-types';
import { Container, Row } from 'react-bootstrap';

import DataGrid from './DataGrid';
import { newcallColumns } from './DataGridColumns';

class NewCallsDataGrid extends React.Component {
  static propTypes = {
    rows: PropTypes.array,
    filters: PropTypes.object,
    onFiltersChange: PropTypes.func,
    onRowsChange: PropTypes.func,
    onAddRow: PropTypes.func,
  };

  render() {
    return (
      <Container className="my-5 ">
        <Row>
          <h4>Capital Drawdow Calculations</h4>
          <p className="text-left"></p>
          <DataGrid
            columns={newcallColumns}
            headerRowHeight={90}
            rows={this.props.rows}
            filters={this.props.filters}
            onFiltersChange={this.props.onFiltersChange}
            onRowsChange={this.props.onRowsChange}
          />
        </Row>
      </Container>
    );
  }
}

export default NewCallsDataGrid;
