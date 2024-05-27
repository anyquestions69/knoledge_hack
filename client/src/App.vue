<template>
  <Header />
  <div>
    <div class="container">
      <div id="result"></div>
      <input class="name" type="text"  placeholder="Название" v-model="title" @keyup.enter="sendMessage">
      <textarea id="text" placeholder="Введите текст" v-model="text" @keyup.enter="sendMessage" rows="3"></textarea>
    </div>
    <div class="send-container">
      <button type="submit" id="send" @click="sendMessage">Отправить текст на анализ</button>
    </div>
</div>

</template>

<script setup>
import Header from './components/Header.vue';
import { ref } from 'vue';

const title = ref('');
const text = ref('');
let socket = new WebSocket("ws://localhost:8000");
const sendMessage = () => {
  const message = JSON.stringify({ text: text.value, title: title.value });
  console.log(message);
  socket.send(JSON.stringify({ text: document.getElementById('text').value, title: document.querySelector('.name').value }));
};



socket.addEventListener("message", (event) => {
  console.log(event.data);
  
  document.getElementById('result').textContent = event.data;
});
 

defineExpose({
  title,
  text,
  sendMessage
});
</script>

<style lang="css" scoped>
@import url('https://fonts.googleapis.com/css2?family=Mulish:ital,wght@0,200..1000;1,200..1000&family=Poetsen+One&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body{
  margin:0;
  padding:0;
}
.container {
  margin-top: auto;
  background: #fcfcfc;
  color: #333;
  padding: 20px;
  height: auto;
  font-family: "Mulish", sans-serif;
  font-optical-sizing: auto;
  font-weight: 500;
  font-style: normal;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  align-items: stretch;
  width: 100%;
}

.name {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  margin: 0;
  color: inherit;
  font-family: inherit;
  font-size: 20px;
  font-weight: inherit;
  line-height: 10px;
  border: none;
  border-radius: 0.4rem;
  transition: box-shadow 100ms;
  margin-bottom: 20px;
  padding: 5px;
}


#result {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  margin: 0;
  color: inherit;
  font-family: inherit;
  font-size: 20px;
  font-weight: inherit;
  line-height: 10px;
  border: none;
  border-radius: 0.4rem;
  transition: box-shadow 100ms;
}

#text {
  margin-top: 30px;
  padding: 5px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  margin: 0;
  color: inherit;
  font-family: inherit;
  font-size: 20px;
  font-weight: inherit;
  line-height: 10px;
  border: none;
  border-radius: 0.4rem;
  transition: box-shadow 100ms;
  height: 300px;
}

.send-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

#send {
  display: inline-block;
  padding: 0.75rem 1.25rem;
  border-radius: 10rem;
  color: #fff;
  text-transform: uppercase;
  font-size: 1rem;
  letter-spacing: 0.15rem;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

/* Исправлено использование переменной $color на прямое значение, так как переменные не поддерживаются напрямую в CSS без предварительной обработки (например, через SASS/SCSS) */
#send::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #007bff; /* Используем прямое значение цвета */
  border-radius: 10rem;
  z-index: -2;
}

#send::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.15); /* Значение для darken($color, 15%) предполагается заменено на прямое значение */
  transition: all 0.3s;
  border-radius: 10rem;
  z-index: -1;
}

#send:hover {
  color: #fff;
}

#send:hover::before {
  width: 100%;
}
</style>

