<template>
  <v-form ref="form" lazy-validation data-test="form-profile">

    <div class="view-header flex-column mb-6">
    <p class="mb-9" v-if="isStepperView">Which products will this account require access to?</p>

      <h4 class="mt-3 payment-page-sub">Select Additional Product(s)</h4>
    </div>
     <template v-if="isLoading">
      <div v-if="isLoading" class="loading-inner-container">
          <v-progress-circular size="50" width="5" color="primary" :indeterminate="isLoading"/>
        </div>
    </template>
    <template v-else>
      <template v-if="avilableProducts && avilableProducts.length > 0">
        <div v-for="product in avilableProducts" :key="product.code">
          <Product
            :productDetails="product"
            @set-selected-product="setSelectedProduct"
            :userName="currentUser.fullName"
            :orgName="currentOrganization.name"
            :isSelectableView="isStepperView"
            :isSelected="currentSelectedProducts.includes(product.code)"
          ></Product>

        </div>
      </template>
      <template v-else>
        <div>No Products are available...</div>
      </template>
    </template>
  <v-divider class="mt-7 mb-10"></v-divider>
    <v-row>
      <v-col cols="12" class="form__btns py-0 d-inline-flex">
        <v-btn
          large
          depressed
          v-if="isStepperView"
          color="default"
          @click="goBack"
          data-test="btn-back"
        >
          <v-icon left class="mr-2">mdi-arrow-left</v-icon>
          <span>Back</span>
        </v-btn>
        <v-spacer></v-spacer>

        <v-btn
          large
          color="primary"
          class="save-continue-button mr-3"
          @click="next"
          v-if="isStepperView"
          data-test="next-button"
          :disabled="!isFormValid"
        >
          <span >
            Next
            <v-icon class="ml-2">mdi-arrow-right</v-icon>
          </span>

        </v-btn>
        <ConfirmCancelButton
          :showConfirmPopup="isStepperView"
          :isEmit="true"
          @click-confirm="cancel"
        ></ConfirmCancelButton>
      </v-col>
    </v-row>

  </v-form>
</template>

<script lang="ts">
import { Component, Mixins, Prop } from 'vue-property-decorator'
import { OrgProduct, Organization } from '@/models/Organization'
import ConfirmCancelButton from '@/components/auth/common/ConfirmCancelButton.vue'
import { KCUserProfile } from 'sbc-common-components/src/models/KCUserProfile'
import NextPageMixin from '@/components/auth/mixins/NextPageMixin.vue'
import Product from '@/components/auth/common/Product.vue'
import { Products } from '@/models/Staff'
import Steppable from '@/components/auth/common/stepper/Steppable.vue'

import { namespace } from 'vuex-class'

const OrgModule = namespace('org')
const userModule = namespace('user')

@Component({
  components: {
    ConfirmCancelButton,
    Product
  }
})
export default class ProductPackages extends Mixins(NextPageMixin, Steppable) {
  @Prop({ default: false }) isStepperView: boolean
  @OrgModule.State('currentOrganization') public currentOrganization!: Organization
  @userModule.State('currentUser') public currentUser!: KCUserProfile
  @OrgModule.State('avilableProducts') public avilableProducts!: OrgProduct[]
  @OrgModule.State('currentSelectedProducts') public currentSelectedProducts!: []

  @OrgModule.Action('getAvilableProducts') public getAvilableProducts!:() =>Promise<Products>
  @OrgModule.Action('addToCurrentSelectedProducts') public addToCurrentSelectedProducts!:(productCode:string) =>Promise<void>

  public isLoading: boolean = false

  $refs: {
    form: HTMLFormElement
  }
  private async setup () {
    this.isLoading = true
    await this.loadProduct()
    this.isLoading = false
  }

  public async mounted () {
    // this.setAccountChangedHandler(this.setup)
    await this.setup()
  }
  public async loadProduct () {
    // No need to load again if already product fetched
    if (!this.avilableProducts || this.avilableProducts.length === 0) {
      const orgProducts = await this.getAvilableProducts()
    }
  }
  get isFormValid () {
    return this.currentSelectedProducts && this.currentSelectedProducts.length > 0
  }

  setSelectedProduct (product) {
    const productCode = product.code
    // adding to store and submit on final click
    this.addToCurrentSelectedProducts(productCode)
  }

  public goBack () {
    this.stepBack()
  }
  public next () {
    this.stepForward()
  }
  private cancel () {
    this.$router.push('/')
  }
}
</script>

<style lang="scss" scoped>
@import '$assets/scss/theme.scss';

</style>
