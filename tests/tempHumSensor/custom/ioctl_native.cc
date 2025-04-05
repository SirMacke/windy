// ioctl_native.cc
#include <node.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <fcntl.h>

namespace ioctl_native {

using v8::FunctionCallbackInfo;
using v8::Isolate;
using v8::Local;
using v8::Object;
using v8::Number;
using v8::Value;

void Ioctl(const FunctionCallbackInfo<Value>& args) {
  Isolate* isolate = args.GetIsolate();

  // Check arguments
  if (args.Length() < 3) {
    isolate->ThrowException(v8::Exception::TypeError(
        v8::String::NewFromUtf8(isolate, "Wrong number of arguments").ToLocalChecked()));
    return;
  }

  if (!args[0]->IsNumber() || !args[1]->IsNumber() || !args[2]->IsNumber()) {
    isolate->ThrowException(v8::Exception::TypeError(
        v8::String::NewFromUtf8(isolate, "Wrong arguments").ToLocalChecked()));
    return;
  }

  int fd = args[0]->Int32Value(isolate->GetCurrentContext()).FromJust();
  unsigned long request = args[1]->IntegerValue(isolate->GetCurrentContext()).FromJust();
  int arg = args[2]->Int32Value(isolate->GetCurrentContext()).FromJust();

  int result = ioctl(fd, request, arg);

  args.GetReturnValue().Set(Number::New(isolate, result));
}

void Initialize(Local<Object> exports) {
  NODE_SET_METHOD(exports, "ioctl", Ioctl);
}

NODE_MODULE(NODE_GYP_MODULE_NAME, Initialize)

}  // namespace ioctl_native