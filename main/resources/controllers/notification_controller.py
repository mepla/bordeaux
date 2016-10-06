

class NotificationControllerBase(object):
    pass


class NotificationController(NotificationControllerBase):
    def notify_new_items(self, new_items):
        print 'There are {} new items:'.format(len(new_items))
        for i in new_items:
            print str(i)
