import Axios from 'axios';

export const SERVER_URL = process.env.REACT_APP_USERS_SERVICE_URL;
console.log(SERVER_URL);

export const getData = endpoint => {
  return Axios.get(`${SERVER_URL}/${endpoint}`)
    .then(res => {
      const data = res.data;
      if (data.status === 'success') {
        return data.data;
      }
    })
    .catch(err => console.log(err));
};

export const sendUpdates = (id, updated) => {
  const url = `${SERVER_URL}/${id}`;
  return Axios.put(url, {
    ...updated,
  })
    .then(res => {
      const data = res.data;
      if (data.status === 'success') {
        return data.data;
      }
    })
    .catch(err => console.log(err));
};

export const sendDelete = id => {
  const url = `${SERVER_URL}/${id}`;
  return Axios.delete(url)
    .then(res => {
      const data = res.data;
      return data.status === 'success' ? true : false;
    })
    .catch(err => console.log(err));
};

export const sendPost = (endpoint, data) => {
  const url = `${SERVER_URL}/${endpoint}`;
  return Axios.post(url, { ...data })
    .then(res => res.data)
    .catch(err => console.log(err));
};
