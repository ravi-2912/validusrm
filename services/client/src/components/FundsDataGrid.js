import React from 'react';
import DataGrid from './DataGrid';
import AddFund from './AddFund';
import { Container, Row, Button } from 'react-bootstrap';
import { ProgressBarFormatter, defaultColumnProperties } from './helper';
import '../css/FundsDataGrid.css';

const columns = [
  {
    key: 'id',
    name: 'ID',
    sortDescendingFirst: true,
    sortable: true,
    width: 120,
    filterable: true,
  },
  {
    key: 'name',
    name: 'Fund Name',
    editable: true,
    sortable: true,
    width: 250,
    filterable: true,
  },
  {
    key: 'invested_committed',
    name: 'Total Invested & Committed',
    sortable: true,
    formatter: ProgressBarFormatter,
  },
  {
    key: 'actions',
    name: 'Actions',
    width: 120,
  },
].map(c => ({ ...c, ...defaultColumnProperties }));

class FundsDataGrid extends React.Component {
  render() {
    return (
      <Container>
        <Row style={{ 'padding-bottom': '50px' }}>
          <h3>Funds Management</h3>
          <p className="desc">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae ipsum iusto placeat.
            Corrupti iste nisi, inventore maiores, nesciunt a similique blanditiis excepturi
            eligendi accusantium minus sit quibusdam molestias, veritatis minima!
          </p>
          <AddFund addToDB={this.props.addFundToDB} />
        </Row>
        <Row>
          <h4>Funds List</h4>
          <p className="desc">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti architecto culpa
            pariatur libero. Iste optio impedit, laudantium odit suscipit eius fugit, ab ipsa
            repellat reprehenderit qui unde nobis fugiat necessitatibus.
          </p>
          <DataGrid
            columns={columns}
            rows={this.props.rows}
            filters={this.props.filters}
            onFiltersChange={this.props.onFiltersChange}
            onRowsChange={this.props.onRowsChange}
            onAddRow={this.props.onAddRow}
            onRowDelete={this.props.onRowDelete}
          />
        </Row>
      </Container>
    );
  }
}

export default FundsDataGrid;
