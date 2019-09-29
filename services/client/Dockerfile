# base image
FROM node:11.12.0-alpine

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH
ENV PATH /usr/src/app/node_modules:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/package.json
COPY package-lock.json /usr/src/app/package-lock.json
RUN npm ci
# RUN npm install react-scripts -g --silent

# copy app
COPY . /usr/src/app

# start app
CMD ["npm", "start"]