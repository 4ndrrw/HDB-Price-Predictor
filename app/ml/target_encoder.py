from typing import List
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class TargetEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, cols: List[str] = None, create_sector: bool = True, sector_len: int = 2):
        self.cols = cols or []
        self.create_sector = create_sector
        self.sector_len = sector_len

    def fit(self, X, y):
        if y is None:
            raise ValueError("y is required to fit TargetEncoder")
        df = X.copy()
        df["_target_"] = y
        self.maps_ = {}
        self.global_means_ = {}

        for c in self.cols:
            s = df.groupby(c)["_target_"].mean()
            self.maps_[c] = s.to_dict()
            self.global_means_[c] = float(s.mean()) if not s.empty else 0.0

        if self.create_sector:
            sector = df["Postcode"].astype(str).str[: self.sector_len]
            s2 = df.assign(Postcode_Sector=sector).groupby("Postcode_Sector")["_target_"].mean()
            self.maps_["Postcode_Sector"] = s2.to_dict()
            self.global_means_["Postcode_Sector"] = float(s2.mean()) if not s2.empty else 0.0

        return self

    def transform(self, X):
        X = X.copy()
        if self.create_sector:
            X["Postcode_Sector"] = X["Postcode"].astype(str).str[: self.sector_len]

        for c in self.cols:
            mapping = self.maps_.get(c, {})
            fallback = self.global_means_.get(c, 0.0)
            X[f"{c}_TE"] = X[c].map(mapping).fillna(fallback).astype(float)

        if self.create_sector:
            mapping = self.maps_.get("Postcode_Sector", {})
            fallback = self.global_means_.get("Postcode_Sector", 0.0)
            X["Postcode_Sector_TE"] = X["Postcode_Sector"].map(mapping).fillna(fallback).astype(float)

        return X