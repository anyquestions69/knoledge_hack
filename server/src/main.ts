import { NestFactory } from '@nestjs/core';
import { NestExpressApplication } from '@nestjs/platform-express';
import { join } from 'path';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create<NestExpressApplication>(AppModule);
  app.useStaticAssets(join(__dirname, '..', 'public'));
  app.setBaseViewsDir(join(__dirname, '..', 'views'));
  app.setViewEngine('hbs');
  app.connectMicroservice({
    transport: Transport.RMQ,
    options: {
      urls: [`localhost`],
      queue: `pupupu`,
      queueOptions: { durable: false },
      prefetchCount: 1,
    },
  });
  
  await app.startAllMicroservices();
  await app.listen(3000);
}
bootstrap();
