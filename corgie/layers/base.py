import torch

STR_TO_LTYPE_DICT  = dict()


def register_layer_type(layer_type_name):
    def register_layer_fn(layer_type):
        STR_TO_LTYPE_DICT[layer_type_name] = layer_type
        return layer_type

    return register_layer_fn


def str_to_layer_type(s):
    global STR_TO_LTYPE_DICT
    return STR_TO_LTYPE_DICT[s]


def get_layer_types():
    return list(STR_TO_LTYPE_DICT.keys())


class BaseLayerType:
    def __init__(self, *kargs, device='cpu', readonly=False, **kwargs):
        super().__init__(*kargs, **kwargs)
        self.device = device
        self.readonly = readonly

    def read(self, dtype=None, **kwargs):
        data_np = self.read_backend(**kwargs)
        # TODO: if np type is unit32, convert it to int64
        data_tens = torch.as_tensor(data_np, device=self.device)
        data_tens = cast_tensor_type(data_tens, dtype)
        return data_tens

    def write(self, data_tens, **kwargs):
        if self.readonly:
            raise Exception("Attempting to write into a readonly layer {}".format(str(self)))
        data_np = data_tens.data.cpu().numpy().astype(
                self.get_data_type()
                )
        self.write_backend(data_np, **kwargs)

    def read_backend(self, *kargs, **kwargs):
        raise NotImplementedError

    def write_backend(self, *kargs, **kwargs):
        raise NotImplementedError

    def get_downsampler(self, *kargs, **kwargs):
        raise NotImplementedError

    def get_upsampler(self, *kargs, **kwargs):
        raise NotImplementedError

    def get_num_channels(self, *kargs, **kwargs):
        raise NotImplementedError

    def convert_data_to_backend(self, *kars, **kwargs):
        raise NotImplementedError

    def convert_data_to_backend(self, *kars, **kwargs):
        raise NotImplementedError


