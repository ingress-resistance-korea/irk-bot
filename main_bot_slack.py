from src.bot_slack.robot import Robot

if '__main__' == __name__:
    print('Initialize Robot Start...')
    robot = Robot()
    try:
        robot.run()
        robot.logger.info('Initialize Robot Complete...')
    except KeyboardInterrupt as e:
        robot.logger.info('Honey Shutdown By User.')
    finally:
        robot.logger.info('Honey Shutdown.')
