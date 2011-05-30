import datetime
import time
import array
import enum


def total_seconds (td):
   # Included in timedelta starting in Python 2.7.
   return float (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

def FormattedTime (delta):
   minutes = delta.seconds / 60
   return "%02d:%02d:%02d" % (minutes       / 60,
                              minutes       % 60,
                              delta.seconds % 60)

TimerState = enum.Enum (["Stopped", "Running", "Completed"])

class Timer:
   def __init__(self):
      self.reset ()
   def start (self):
      self.state = TimerState.Running
      self.started = datetime.datetime.now ()
      # We add a fudge second to make the time remaining look correct,
      # in place of displaying the ceiling of the fractional seconds.
      if self.duration is not None:
         self.ending = self.started + self.duration + datetime.timedelta(seconds=1)
   def reset (self):
      self.state    = TimerState.Stopped
      self.started  = None
      self.duration = None
      self.ending   = None
   def running (self):
      return self.state == TimerState.Running
      #return self.started is not None
   def setduration (self, duration):
      if self.state == TimerState.Running:
         raise Exception ("Can't set duration while running.")
      else:
         self.duration = duration
   def timeelapsed(self):
      if self.state == TimerState.Completed:
         return FormattedTime(self.duration)
      if self.ending is not None and datetime.datetime.now () >= self.ending:
         self.state = TimerState.Completed

         return FormattedTime(self.duration)
      elif self.started is None:
         return FormattedTime(datetime.timedelta (0))
      else:
         return FormattedTime(datetime.datetime.now() - self.started)
   def timeremaining(self):
      if self.ending is not None and datetime.datetime.now () >= self.ending:
         self.state = TimerState.Completed

         return FormattedTime(datetime.timedelta(0))
      elif self.started is None and self.duration is not None:
         return FormattedTime(self.duration);
      elif self.ending is None:
         return FormattedTime(datetime.timedelta(0))
      else:
         return FormattedTime(self.ending - datetime.datetime.now())
   def progress(self):
      if datetime.datetime.now () >= self.ending:
         self.state = TimerState.Completed
      elif self.started is None or self.duration is None or self.duration == 0:
         return 0.0
      else:
         return total_seconds(datetime.datetime.now() - self.started) / total_seconds(self.duration)
   def secondsremaining (self):
      if datetime.datetime.now () >= self.ending:
         self.state = TimerState.Completed
      elif self.started is None or self.duration is None:
         return 0
      else:
         return total_seconds(self.ending - datetime.datetime.now() )
   def __str__(self):
      return "Time elapsed: " + self.timeelapsed () + "\n" + \
             "Time remaining: " + self.timeremaining() + "\n" + \
             ("Progress: %2f" % self.progress())

class TimeInput:
   def __init__(self):
      self.clear ()
   def clear (self):
      self.digits = '0'*6
   def append(self, key):
      if key.isdigit ():
         self.digits = self.digits[1:] + key
      else:
         raise ValueError ("Could not append '" + key + "' to TimeInput object")
   def duration(self):
      return datetime.timedelta(hours=int(self.digits[0:2]),minutes=int(self.digits[2:4]),seconds=int(self.digits[4:6]) )
   def durationstring (self):
      return FormattedTime (self.duration () )
   def durationUntil (self):
      # self.duration represents a target time, not a time delta.
      target_seconds = int(total_seconds (self.duration () ) )
      target_time = datetime.datetime.now ().replace \
         (hour=target_seconds / 60 / 60, minute=target_seconds / 60 % 60, second=target_seconds % 60)
      if target_time <= datetime.datetime.now ():
         raise ValueError ("Time entered has already occured.")
      return target_time - datetime.datetime.now()
   def tostring (self):
      return self.digits [0:2] + ':' + self.digits [2:4] + ':' + self.digits [4:6]
   def __str__(self):
      return self.tostring ()

if __name__ == '__main__':
   print "Timer demo"
   timer1 = Timer ()
   timer1.setduration(datetime.timedelta(minutes=10) )
   print timer1
   timer1.start ()
   for I in range (10):
      time.sleep (1)
      print timer1
