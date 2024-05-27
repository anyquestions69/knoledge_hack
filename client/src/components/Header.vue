<template>
    <div class="header">
        <img class="logo" src="C:\Users\ilya\Desktop\projects\FS_course\clien\src\assets\icons\icon.png" alt="Logo" />
        <span class="title">Анализ полноты содержания статей на основе искусственного интеллекта</span>
        <img class="star" src="C:\Users\ilya\Desktop\projects\FS_course\clien\src\assets\icons\star.png" alt="Logo" />
    </div>
</template>
<script>
export default {
    name: "Header",
    
    props: {
        title: {
            type: String,
        }
    },
};
</script>

<style lang="css" scoped>
@import url('https://fonts.googleapis.com/css2?family=Mulish:ital,wght@0,200..1000;1,200..1000&family=Poetsen+One&display=swap');

.header {
    background: #333;
    color: #fff;
    padding: 20px;
    border-bottom: 2px solid #000;
    height: 120px;
    font-family: "Mulish", sans-serif;
    font-optical-sizing: auto;
    font-weight: 500;
    font-style: medium;
    display: flex; 
    justify-content: space-between; 
    align-items: center;
}

.header .logo {
    margin-right: 10px; 
    width: 140px;
    height: 100px;
}

.header .title {
    font-size: 28px;
    text-align: right;
}

.header .star {
    margin-right: 10px; 
    width: 70px;
    height: 70px;
    /* flex-grow: 1; */
}

</style>