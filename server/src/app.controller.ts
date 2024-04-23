import { Body, Controller, Get, Post, Render } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  @Render('index')
  root() {
    return ;
  }
  @Post('check')
  async name(@Body()text:string) {
    return await this.appService.check(text);
  }
}
